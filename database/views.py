from django.contrib.auth import authenticate, login, logout
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse, HttpResponseServerError, HttpResponseNotFound
from django.db import IntegrityError
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Group as AuthGroup
from django.db.models import Prefetch

import MySQLdb as mdb
import psycopg2
import cx_Oracle
import oracledb
# import pyodbc
from pymongo import MongoClient

import csv
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse, HttpResponseServerError, HttpResponseNotFound
from django.db import IntegrityError
from django.core.exceptions import ValidationError
# from django.core.validators import validate_email
import json

from database.password_generator import PasswordGenerator
from database.sender import EmailSender
from .serializers import UserSerializer, TeacherSerializer, DetailedTeacherSerializer, StudentSerializer, DetailedStudentSerializer, MajorSerializer, CourseSerializer, SemesterSerializer, BasicSemesterSerializer, EditionSerializer, BasicEditionSerializer, TeacherEditionSerializer, GroupSerializer, DetailedGroupSerializer, DBMSSerializer, GroupSerializerForStudent, ServerSerializer, EditionServerSerializer, DBAccountSerializer
# , SimpleTeacherEditionSerializer
from .models import User, Teacher, Student, Major, Course, Semester, Edition, TeacherEdition, Group, DBMS, Server, EditionServer, DBAccount


SYSTEM_NAME = 'PUT DB 2023'

INVALID_EMAIL = 'Niepoprawny adres email.'
EMAIL_DUPLICATED = 'Podany adres email jest już zajęty.'
MISSING_FIELDS = 'Nie podano wszystkich wymaganych pól.'

NEW_USER_SUBJECT = f'Konto w systemie {SYSTEM_NAME}'
NEW_USER_MESSAGE = f'Twoje konto w systemie {SYSTEM_NAME} zostało utworzone. Twoje dane do logowania to:'
RESET_PASSWORD_SUBJECT = f'Reset hasław systemie {SYSTEM_NAME}'
RESET_PASSWORD_MESSAGE = 'Twoje hasło do konta zostało zresetowane. Nowe dane logowania to:'


class UserViewSet(ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting users.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'email', 'first_name', 'last_name', 'is_student', 'is_teacher', 'is_staff', 'is_superuser', 'is_active']

    def get_queryset(self):
        user = self.request.user
        if not user.has_perm('database.view_user'):
            raise PermissionDenied

        if user.is_superuser:
            return User.objects.all()
        return User.objects.filter(id=user.id)


    def create(self, request, *args, **kwargs):
        # print("Creating admin...")
        user = request.user
        if not user.has_perm('database.add_user'):
            raise PermissionDenied()
            
        # create superuser
        if not user.is_superuser:
            raise PermissionDenied()
        
        if not user._validate_email(request.data['email']):
            return JsonResponse({'name': INVALID_EMAIL}, status=400)

        password = User.objects.make_random_password(length=10)
        print(f"Email: {request.data['email']}\nPassword: {password}")
        
        new_superuser = User.objects.create_superuser(
            email=request.data['email'],
            password=password,
            first_name=request.data['first_name'],
            last_name=request.data['last_name'],
            *args, **kwargs)
        print('superuser created:', new_superuser)
        return Response(UserSerializer(new_superuser).data, status=201)

    def update(self, request, *args, **kwargs):
        user = request.user
        if not user.has_perm('database.change_user'):
            raise PermissionDenied()
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        if not user.has_perm('database.delete_user'):
            raise PermissionDenied()
        return super().destroy(request, *args, **kwargs)


class TeacherViewSet(ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting teachers.
    """
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'id',
        'user',
        'user__email',
        'user__first_name',
        'user__last_name',
        'editions__semester',
        'editions__semester__start_year',
        'editions__semester__winter',
        'editions__semester__active',
        'editions__course',
        'editions__course__name',
    ]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailedTeacherSerializer
        return TeacherSerializer

    def grant_teacher_permissions(self, user):
        teacher_group = AuthGroup.objects.get(name='TeacherGroup')
        user.groups.add(teacher_group)

    def get_queryset(self):
        user = self.request.user
        if not user.has_perm('database.view_teacher'):
            raise PermissionDenied

        if user.is_superuser:
            return Teacher.objects.all()
        elif user.is_teacher:
            teacher = get_object_or_404(Teacher, user=self.request.user)
            return Teacher.objects.all().filter(id=teacher.id)
        elif user.is_student:
            student = get_object_or_404(Student, user=self.request.user)
            print('Debug: ', Teacher.objects.all().filter(teacheredition__groups__students=student).distinct())
            return Teacher.objects.all().filter(teacheredition__groups__students=student).distinct()
        else:
            return Teacher.objects.none()

    def create(self, request, *args, **kwargs):
        user = request.user
        if not user.has_perm('database.add_teacher'):
            raise PermissionDenied()

        # check if request.data contains fields from user model
        if 'email' in request.data and 'first_name' in request.data and 'last_name' in request.data:
            if not user._validate_email(request.data['email']):
                return JsonResponse({'name': INVALID_EMAIL}, status=400)
            try:
                new_password = User.objects.make_random_password(length=10)
                print(f"Email: {request.data['email']}\nPassword: {new_password}")
                user = User.objects.create_user(
                    email=request.data['email'],
                    first_name=request.data['first_name'],
                    last_name=request.data['last_name'],
                    password = new_password,
                    is_teacher=True,
                )
                TeacherViewSet.grant_teacher_permissions(self, user)
                teacher = Teacher.objects.create(user=user)
                user.send_email_gmail(NEW_USER_SUBJECT, NEW_USER_MESSAGE, new_password)
                return Response(TeacherSerializer(teacher).data, status=201)
            except IntegrityError:
                return JsonResponse({'name': EMAIL_DUPLICATED}, status=400)
            except ValidationError:
                return JsonResponse({'name': INVALID_EMAIL}, status=400)
            except Exception as e:
                return JsonResponse({'name': str(e)}, status=400)
        else:
            return JsonResponse({'name': MISSING_FIELDS}, status=400)

    def update(self, request, *args, **kwargs):
        user = request.user
        if not user.has_perm('database.change_teacher'):
            raise PermissionDenied()

        print(f"request.data {request.data}")
        # check if request.data contains fields from user model
        if 'email' in request.data and 'first_name' in request.data and 'last_name' in request.data:
            try:
                teacher = self.get_object()
                user = teacher.user
                user.email = request.data['email']
                user.first_name = request.data['first_name']
                user.last_name = request.data['last_name']
                user.save()
                return Response(TeacherSerializer(teacher).data)
            except IntegrityError:
                return JsonResponse({'name': EMAIL_DUPLICATED}, status=400)
            except ValidationError:
                return JsonResponse({'name': INVALID_EMAIL}, status=400)
            except Exception as e:
                return JsonResponse({'name': str(e)}, status=400)
        else:
            return JsonResponse({'name': MISSING_FIELDS}, status=400)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        if not user.has_perm('database.delete_teacher'):
            raise PermissionDenied()

        # delete user
        teacher = self.get_object()
        user = teacher.user
        user.delete()
        # delete teacher
        teacher.delete()
        return Response(status=204)
        

class StudentViewSet(ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting students.
    """
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'id',
        'user',
        'user__email',
        'user__first_name',
        'user__last_name',
        'student_id',
        'groups',
        'groups__name',
        'db_accounts__editionServer__server',
        'db_accounts__editionServer__server__name',
    ]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailedStudentSerializer
        return StudentSerializer

    def grant_student_permissions(self, user):
        student_group = AuthGroup.objects.get(name='StudentGroup')
        user.groups.add(student_group)

    def get_queryset(self):
        user = self.request.user  
        if not user.has_perm('database.view_student'):
            raise PermissionDenied

        if user.is_superuser:
            return Student.objects.all()
        elif user.is_teacher:
            teacher = Teacher.objects.get(user=user)
            groups = Group.objects.filter(teacherEdition__teacher=teacher)
            students = Student.objects.filter(groups__teacherEdition__teacher=teacher).prefetch_related(Prefetch('groups', queryset=groups))
            return students.distinct()
        elif user.is_student:
            return Student.objects.filter(user=user)
        else:
            return Student.objects.none()

    def create(self, request, *args, **kwargs):
        user = request.user
        if not user.has_perm('database.add_student'):
            raise PermissionDenied()
        
        # check if request.data contains fields from user model
        if 'email' in request.data and 'first_name' in request.data and 'last_name' in request.data and 'student_id' in request.data and 'major' in request.data:
            if not user._validate_email(request.data['email']):
                return JsonResponse({'name': INVALID_EMAIL}, status=400)
            try:
                new_password = User.objects.make_random_password()
                print(f"email: {request.data['email']}, password: {new_password}")
                user = User.objects.create_user(
                    email=request.data['email'],
                    first_name=request.data['first_name'],
                    last_name=request.data['last_name'],
                    password=new_password,
                    is_student=True,
                )
                self.grant_student_permissions(user)
                major = Major.objects.get(id=request.data['major'])
                student = Student.objects.create(user=user, student_id=request.data['student_id'], major=major)
                user.send_email_gmail(NEW_USER_SUBJECT, NEW_USER_MESSAGE, new_password)
                return Response(StudentSerializer(student).data, status=201)
            except IntegrityError:
                return JsonResponse({'name': EMAIL_DUPLICATED}, status=400)
            except ValidationError:
                return JsonResponse({'name': INVALID_EMAIL}, status=400)
            except Exception as e:
                return JsonResponse({'name': str(e)}, status=400)
        else:
            return JsonResponse({'name': MISSING_FIELDS}, status=400)

    def update(self, request, *args, **kwargs):
        user = request.user
        if not user.has_perm('database.change_student'):
            raise PermissionDenied()

        print(f"request.data {request.data}")
        # check if request.data contains fields from user model
        if 'email' in request.data and 'first_name' in request.data and 'last_name' in request.data and 'student_id' in request.data:
            try:
                student = self.get_object()
                user = student.user
                user.email = request.data['email']
                user.first_name = request.data['first_name']
                user.last_name = request.data['last_name']
                user.save()
                student.student_id = request.data['student_id']
                student.save()
                return Response(StudentSerializer(student).data)
            except IntegrityError:
                return JsonResponse({'name': EMAIL_DUPLICATED}, status=400)
            except ValidationError:
                return JsonResponse({'name': INVALID_EMAIL}, status=400)
            except Exception as e:
                return JsonResponse({'name': str(e)}, status=400)
        else:
            return JsonResponse({'name': MISSING_FIELDS}, status=400)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        if not user.has_perm('database.delete_student'):
            raise PermissionDenied()

        # delete user
        student = self.get_object()
        user = student.user
        user.delete()
        # delete student
        # student.delete()
        return Response(status=204)


class MajorViewSet(ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting majors.
    """
    serializer_class = MajorSerializer
    queryset = Major.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'name', 'courses', 'courses__name']

    def create(self, request, *args, **kwargs):
        user = request.user
        if not user.has_perm('database.add_major'):
            raise PermissionDenied()
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        user = request.user
        if not user.has_perm('database.change_major'):
            raise PermissionDenied()
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        if not user.has_perm('database.delete_major'):
            raise PermissionDenied()
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if not user.has_perm('database.view_major'):
            raise PermissionDenied
        return Major.objects.all()


class CourseViewSet(ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting courses.
    """
    serializer_class = CourseSerializer
    queryset = Course.objects.all().order_by('id')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'name', 'major', 'active', 'description', 'editions']

    def update(self, request, *args, **kwargs):
        user = request.user
        if not user.has_perm('database.change_course'):
            raise PermissionDenied
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        if not user.has_perm('database.delete_course'):
            raise PermissionDenied
        return super().destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        user = request.user
        if not user.has_perm('database.add_course'):
            raise PermissionDenied
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if not user.has_perm('database.view_course'):
            raise PermissionDenied

        if user.is_superuser:
            return Course.objects.all().order_by('id')
        elif user.is_teacher:
            teacher = get_object_or_404(Teacher, user=self.request.user)
            return Course.objects.all().filter(editions__teachers=teacher).order_by('id').distinct()
        elif user.is_student:
            student = get_object_or_404(Student, user=self.request.user)
            return Course.objects.all().filter(editions__teacheredition__groups__students=student).order_by('id').distinct()
        else:
            return Course.objects.none()


class SemesterViewSet(ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting semesters.
    """
    serializer_class = SemesterSerializer
    queryset = Semester.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'start_year', 'winter', 'active', 'editions']

    def create(self, request, *args, **kwargs):
        user = request.user
        if not user.has_perm('database.add_semester'):
            raise PermissionDenied()

        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError as error:
            if "unique_semester" in str(error):
                return HttpResponseBadRequest(json.dumps({'name': 'Semestr już istnieje.'}), headers={'Content-Type': 'application/json'})
            return HttpResponseBadRequest(json.dumps({'name': str(error)}), headers={'Content-Type': 'application/json'})

    def update(self, request, *args, **kwargs):
        user = request.user
        if not user.has_perm('database.change_semester'):
            raise PermissionDenied()

        if request.data.get('active') == True:
            Semester.objects.all().update(active=False)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        if not user.has_perm('database.delete_semester'):
            raise PermissionDenied()

        semester = self.get_object()
        if semester.active:
            return HttpResponseBadRequest(json.dumps({'name': 'Nie można usunąć aktywnego semestru.'}), headers={'Content-Type': 'application/json'})
        if semester.editions.count() > 0:
            return HttpResponseBadRequest(json.dumps({'name': 'Nie można usunąć semestru, który ma przypisane edycje.'}), headers={'Content-Type': 'application/json'})
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if not user.has_perm('database.view_semester'):
            raise PermissionDenied

        return Semester.objects.all()


class SimpleSemesterViewSet(ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting semesters.
    """
    serializer_class = BasicSemesterSerializer
    queryset = Semester.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'id',
        'start_year',
        'winter',
        'active',
        'editions'
    ]


class EditionViewSet(ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting editions.
    """
    serializer_class = EditionSerializer
    queryset = Edition.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'id', 
        'description', 
        'date_opened', 
        'date_closed',
        'semester', 
        'semester__start_year', 
        'semester__winter', 
        'semester__active',
        'course', 
        'course__name',
        'course__description',
        'teachers',
        'teachers__user__first_name',
        'teachers__user__last_name',
    ]

    def create(self, request, *args, **kwargs):
        user = request.user
        if not user.has_perm('database.add_edition'):
            raise PermissionDenied

        teachers = request.data['teachers']
        servers = request.data['servers']

        try:
            print("Creating edition")
            edition = Edition.objects.create(
                course=Course.objects.get(id=request.data['course']),
                semester=Semester.objects.get(id=request.data['semester']),
                description=request.data['description'],
                date_opened=request.data['date_opened'],
                date_closed=request.data['date_closed'],
            )
            print(f"Edition created: {edition}")

            TeacherEdition.objects.bulk_create([
                TeacherEdition(teacher=Teacher.objects.get(id=teacher), edition=edition)
                for teacher in teachers
            ])
            print(f"Teachers added: {teachers}")
            EditionServer.objects.bulk_create([
                EditionServer(server=Server.objects.get(id=server), edition=edition)
                for server in servers
            ])
            print(f"Servers added: {servers}")
            return Response(EditionSerializer(edition).data)
            # super().create(request, *args, **kwargs)
        except IntegrityError as error:
            if "unique_edition" in str(error):
                return HttpResponseBadRequest(json.dumps({'name': 'Edycja już istnieje.'}), headers={'Content-Type': 'application/json'})
        except Exception as error:
            return HttpResponseBadRequest(json.dumps({'name': str(error)}), headers={'Content-Type': 'application/json'})

    def update(self, request, *args, **kwargs):
        user = request.user
        if not user.has_perm('database.change_edition'):
            raise PermissionDenied

        if 'teachers' not in request.data:
            return HttpResponseBadRequest(json.dumps({'name': 'Nie podano nauczycieli.'}), headers={'Content-Type': 'application/json'})
        if 'servers' not in request.data:
            return HttpResponseBadRequest(json.dumps({'name': 'Nie podano serwerów.'}), headers={'Content-Type': 'application/json'})
        try:
            # print(f"Updating edition {request.data['id']}")
            teachers = request.data['teachers']
            servers = request.data['servers']

            edition = Edition.objects.get(id=self.get_object().id)
            edition.course = Course.objects.get(id=request.data['course'])
            edition.semester = Semester.objects.get(id=request.data['semester'])
            edition.description = request.data['description']
            edition.date_opened = request.data['date_opened']
            edition.date_closed = request.data['date_closed']

            current_teachers = [teacher.id for teacher in edition.teachers.all()]

            # check if missing teachers do not have any groups in this edition
            for current_teacher in current_teachers:
                if current_teacher not in teachers:
                    teacher_edition = TeacherEdition.objects.get(teacher=current_teacher, edition=edition)
                    print(f"Teacher edition: {teacher_edition}")
                    if Group.objects.filter(teacherEdition=teacher_edition).exists():
                        return HttpResponseBadRequest(json.dumps({'name': 'Nie można usunąć nauczyciela, który ma przypisane grupy.'}), headers={'Content-Type': 'application/json'})

            edition.teachers.set(teachers)
            edition.servers.set(servers)

            edition.save()
            print(f"Edition updated: {edition}")

            return Response(EditionSerializer(edition).data, status=200)
            # super().update(request, *args, **kwargs)
        except IntegrityError as error:
            if "unique_edition" in str(error):
                return HttpResponseBadRequest(json.dumps({'name': 'Edycja już istnieje.'}), headers={'Content-Type': 'application/json'})
            return HttpResponseBadRequest(json.dumps({'name': str(error)}), headers={'Content-Type': 'application/json'})

    def destroy(self, request, *args, **kwargs):   
        user = request.user
        if not user.has_perm('database.delete_edition'):
            raise PermissionDenied

        try:
            teacher_editions = TeacherEdition.objects.filter(edition=self.get_object().id)
            if teacher_editions.exists():
                for teacher_edition in teacher_editions:
                    if Group.objects.filter(teacherEdition=teacher_edition).exists():
                        return HttpResponseBadRequest(json.dumps({'name': 'Edycja ma przypisane grupy.'}), headers={'Content-Type': 'application/json'})
            edition = Edition.objects.get(id=self.get_object().id)
            edition.delete()
            return Response(status=204)
        except Exception as error:
            return HttpResponseBadRequest(json.dumps({'name': str(error)}), headers={'Content-Type': 'application/json'})
    
    def get_queryset(self):
        user = self.request.user
        if not user.has_perm('database.view_edition'):
            raise PermissionDenied

        if user.is_superuser:
            return Edition.objects.order_by('id')
        elif user.is_teacher:
            teacher = get_object_or_404(Teacher, user=self.request.user)
            return Edition.objects.filter(teachers=teacher).order_by('id').distinct()
        elif user.is_student:
            student = get_object_or_404(Student, user=self.request.user)
            return Edition.objects.filter(teacheredition__groups__students=student).order_by('id').distinct()
        else:
            return Edition.objects.none()


class TeacherEditionViewSet(ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting teachers in editions.
    """
    serializer_class = TeacherEditionSerializer
    queryset = TeacherEdition.objects.all().order_by('id')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'id',
        'teacher',
        'edition',
        'edition__description',
        'edition__date_opened',
        'edition__date_closed',
        'edition__course',
        'edition__semester',
        'edition__semester__start_year',
        'edition__semester__winter',
        'edition__semester__active',
        'edition__course__name',
        'teacher',
        'teacher__user__first_name',
        'teacher__user__last_name',
    ]

    def get_queryset(self):
        user = self.request.user
        if not user.has_perm('database.view_teacheredition'):
            raise PermissionDenied

        if user.is_superuser:
            return super().get_queryset()
        elif user.is_teacher:
            teacher = get_object_or_404(Teacher, user=self.request.user)
            print(f"Teacher: {teacher}")
            return TeacherEdition.objects.filter(teacher=teacher).order_by('id')
        elif user.is_student:
            student = get_object_or_404(Student, user=self.request.user)
            return TeacherEdition.objects.filter(edition__groups__students=student).order_by('id')

        return TeacherEdition.objects.none()

    def create(self, request, *args, **kwargs):
        user = request.user
        if not user.has_perm('database.add_teacheredition'):
            raise PermissionDenied
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        user = request.user
        if not user.has_perm('database.change_teacheredition'):
            raise PermissionDenied
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        if not user.has_perm('database.delete_teacheredition'):
            raise PermissionDenied
        return super().destroy(request, *args, **kwargs)


class GroupViewSet(ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting groups.
    """
    serializer_class = GroupSerializer
    queryset = Group.objects.all().order_by('id')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'id', 
        'name', 
        'day', 
        'hour', 
        'room', 
        'teacherEdition', 
        'teacherEdition__edition', 
        'teacherEdition__edition__semester', 
        'teacherEdition__edition__semester__start_year', 
        'teacherEdition__edition__semester__winter',
        'teacherEdition__edition__semester__active',
        'teacherEdition__edition__course', 
        'teacherEdition__edition__course__name',
        'teacherEdition__edition__servers',
        'teacherEdition__edition__servers__name',
        'teacherEdition__edition__servers__host',
        'teacherEdition__edition__servers__port',
        'teacherEdition__edition__servers__active',
        'teacherEdition__teacher', 
        'teacherEdition__teacher__user__first_name', 
        'teacherEdition__teacher__user__last_name',
    ]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailedGroupSerializer
        return GroupSerializer

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        if not user.has_perm('database.view_group'):
            raise PermissionDenied

        group = self.get_object()
        serializer = self.get_serializer(group)
        all_accounts_moved = True
        resp = serializer.data

        if not user.is_student:
            for student in group.students.all():
                for server in group.teacherEdition.edition.servers.all():
                    if not student.db_accounts.filter(editionServer__server=server).exists():
                        all_accounts_moved = False
                        break
                for db_account in student.db_accounts.all():
                    if db_account.is_moved == False:
                        all_accounts_moved = False
                        break
                if all_accounts_moved == False:
                    break
            resp['all_accounts_moved'] = all_accounts_moved
        return Response(resp, status=200)
    
    # filter against current user
    def get_queryset(self):
        user = self.request.user
        if not user.has_perm('database.view_group'):
            raise PermissionDenied

        if user.is_superuser:
            return Group.objects.order_by('id')
        elif user.is_teacher:
            teacher = get_object_or_404(Teacher, user=user)
            return Group.objects.filter(teacherEdition__teacher=teacher).order_by('id').distinct()
        elif user.is_student:
            # student = get_object_or_404(Student, user=user)
            # return Group.objects.filter(students=student).order_by('id').distinct()
            student = Student.objects.filter(user=user)
            groups = Group.objects.all().filter(students=student[0]).prefetch_related(Prefetch('students', queryset=student))
            return groups.order_by('id').distinct()
        else:
            return Group.objects.none()


class DBMSViewSet(ModelViewSet):
    serializer_class = DBMSSerializer
    queryset = DBMS.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'id',
        'name',
        'description',
        'servers',
    ]

    def create(self, request, *args, **kwargs):
        user = request.user
        if not user.has_perm('database.add_dbms'):
            raise PermissionDenied()
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        user = request.user
        if not user.has_perm('database.change_dbms'):
            raise PermissionDenied()
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        if not user.has_perm('database.delete_dbms'):
            raise PermissionDenied()
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if not user.has_perm('database.view_dbms'):
            raise PermissionDenied
        return super().get_queryset()


class ServerViewSet(ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting servers.
    """
    raise_exception = True
    serializer_class = ServerSerializer
    queryset = Server.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'id', 
        'name',
        'host', 
        'port', 
        'date_created', 
        'active',
        'editions', 
        'editions__description', 
        'editions__date_opened', 
        'editions__date_closed', 
        'editions__semester', 
        'editions__semester__start_year', 
        'editions__semester__winter', 
        'editions__semester__active',
        'editions__course',
        'editions__course__name', 
        'editions__course__description',
    ]

    def get_queryset(self):
        user = self.request.user
        if not user.has_perm('database.view_server'):
            raise PermissionDenied
        return super().get_queryset()

    def destroy(self, request, *args, **kwargs):
        user = request.user
        if not user.has_perm('database.delete_server'):
            raise PermissionDenied
        return super().destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        user = request.user
        if not user.has_perm('database.add_server'):
            raise PermissionDenied
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        user = request.user
        if not user.has_perm('database.change_server'):
            raise PermissionDenied
        return super().update(request, *args, **kwargs)


class EditionServerViewSet(ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting edition servers.
    """
    serializer_class = EditionServerSerializer
    queryset = EditionServer.objects.select_related('server', 'edition__semester', 'edition__course').order_by('id')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'id', 
        'additional_info',
        'edition',
        'edition__description', 
        'edition__date_opened', 
        'edition__date_closed', 
        'edition__semester', 
        'edition__semester__start_year', 
        'edition__semester__winter', 
        'edition__semester__active',
        'edition__course',
        'edition__course__name', 
        'server', 
        'server__name', 
        'server__ip', 
        'server__port', 
        'server__date_created', 
        'server__active',
    ]

    def get_queryset(self):
        user = self.request.user
        if not user.has_perm('database.view_editionserver'):
            raise PermissionDenied
        return super().get_queryset()

    def destroy(self, request, *args, **kwargs):
        user = request.user
        if not user.has_perm('database.delete_editionserver'):
            raise PermissionDenied
        return super().destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        user = request.user
        if not user.has_perm('database.add_editionserver'):
            raise PermissionDenied
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        user = request.user
        if not user.has_perm('database.change_editionserver'):
            raise PermissionDenied
        return super().update(request, *args, **kwargs)


class DBAccountViewSet(ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting db accounts.
    """
    serializer_class = DBAccountSerializer
    queryset = DBAccount.objects.select_related('student', 'editionServer__server', 'editionServer__edition__semester', 'editionServer__edition__course').order_by('id')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'id', 
        'username', 
        'password', 
        'additional_info',
        'is_moved',
        'editionServer', 
        'editionServer__edition',
        'editionServer__edition__course',
        'editionServer__edition__semester',
        'editionServer__edition__semester__start_year',
        'editionServer__edition__semester__winter',
        'editionServer__edition__semester__active',
        'editionServer__edition__course__name',
        'editionServer__server',
        'editionServer__server__name',
        'editionServer__server__active',
        'student',
        'student__user__first_name',
        'student__user__last_name',
        'student__student_id',
    ]

    def get_queryset(self):
        user = self.request.user
        if not user.has_perm('database.view_dbaccount'):
            raise PermissionDenied
        
        if user.is_teacher:
            return super().get_queryset().filter(editionServer__edition__course__teacher=user.teacher)
        elif user.is_student:
            return super().get_queryset().filter(student=user.student)

        return super().get_queryset()

    def destroy(self, request, *args, **kwargs):
        user = request.user
        if not user.has_perm('database.delete_dbaccount'):
            raise PermissionDenied
        
        if user.is_teacher:
            account = self.get_object()
            if account.editionServer.edition.course.teacher != user.teacher:
                raise PermissionDenied

        return super().destroy(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        user = request.user
        if not user.has_perm('database.add_dbaccount'):
            raise PermissionDenied


class LoginView(ViewSet):
    def get_permissions(self):
        if self.action == 'login_user':
            return [AllowAny()]
        return [IsAuthenticated()]

    @action (methods=['post'], detail=False)
    def login_user(self, request, format=None):
        login_data = request.data
        print('Request log:', login_data)
        # print('Request headers:', request.headers)
        user = authenticate(email=login_data['email'], password=login_data['password'])
        if user is not None:
            login(request, user)
            print(user.get_all_permissions())
            return JsonResponse(
                {
                    'name': 'Udało się zalogować.',
                    'user': {
                        'id': user.id,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'email': user.email,
                        'is_student': user.is_student,
                        'is_teacher': user.is_teacher,
                        'is_superuser': user.is_superuser,
                        'permissions': list(user.get_all_permissions()),
                    }
                }, status=200)
        else:
            return HttpResponseBadRequest(json.dumps({'name': 'Niepoprawne dane logowania.'}), headers={'Content-Type': 'application/json'})


class LogoutView(ViewSet):
    def get_permissions(self):
        if self.action == 'logout_user':
            return [AllowAny()]
        return [IsAuthenticated()]

    @action (methods=['post'], detail=False)
    def logout_user(self, request, format=None):
        print('logout', request)
        logout(request)
        return Response({'name': 'Nastąpiło poprawne wylogowanie.'}, status=200)


class AddUserAccountToExternalDB(ViewSet):
    def mysql(self, server, db_accounts):
        moved_accounts = []
        try:
            conn_mysql = mdb.connect(
                host=server.host,
                port=int(server.port),
                user=server.user,
                passwd=server.password,
                db=server.database
            )
            cursor = conn_mysql.cursor()
            print('Connected to MySQL server')
            for account in db_accounts:
                print(server.create_user_template)
                cursor.execute("SELECT user FROM mysql.user WHERE user = '%s'" % (account.username))
                user_exists = cursor.fetchone()
                if user_exists:
                    print(f"User '{account.username}' already exists in database.")
                    DBAccount.objects.filter(id=account.id).update(is_moved=True)
                    continue
                else:
                    cursor.execute(server.create_user_template % (account.username, account.password))
                    moved_accounts.append(account.username)
                    DBAccount.objects.filter(id=account.id).update(is_moved=True)
                    print(f"Successfully created user '{account.username}' with '{account.password}' password.")
            conn_mysql.commit()
            cursor.close()
            conn_mysql.close()
            return JsonResponse({'moved_accounts': moved_accounts}, status=200)
        except (Exception, mdb.DatabaseError) as error:
            print("error: ", error)
            if error.args[0] == 2002:
                return HttpResponseBadRequest(json.dumps({'name': f"Nie udało się połączyć z serwerem baz danych ({server.name} - {server.dbms.name})."}), headers={'Content-Type': 'application/json'})
            return JsonResponse({'name': str(error)}, status=500)
    
    def postgresql(self, server, db_accounts):
        moved_accounts = []
        try:
            conn_postgres = psycopg2.connect(
                dbname=server.database,
                user=server.user,
                password=server.password,
                host=server.host,
                port=server.port
            )
            print('Connected to Postgres server')
            cursor = conn_postgres.cursor()
            for account in db_accounts:
                print(account.username)
                cursor.execute('SELECT rolname FROM pg_roles WHERE rolname = %s', (account.username,))
                user_exists = cursor.fetchone()
                if user_exists:
                    print(f"User '{account.username}' already exists in database.")
                    DBAccount.objects.filter(id=account.id).update(is_moved=True)
                    continue
                else:
                    cursor.execute(server.create_user_template % (account.username, account.password))
                    moved_accounts.append(account.username)
                    DBAccount.objects.filter(id=account.id).update(is_moved=True)
                    print(f"Successfully created user '{account.username}' with '{account.password}' password.")
            conn_postgres.commit()
            cursor.close()
            conn_postgres.close()
            return JsonResponse({'moved_accounts': moved_accounts}, status=200)
        except Exception as error:
            print(error)
            if 'could not connect to server' in str(error):
                return HttpResponseBadRequest(json.dumps({'name': f"Nie udało się połączyć z serwerem baz danych ({server.name} - {server.dbms.name})."}), headers={'Content-Type': 'application/json'})
            return JsonResponse({'name': str(error)}, status=500)
    
    def mongodb(self, server, db_accounts):
        moved_accounts = []
        try:
            conn = MongoClient(f'mongodb://{server.user}:{server.password}@{server.host}:{server.port}/')
            db = conn[server.database]
            for account in db_accounts:
                # print(account.username)
                listing = db.command('usersInfo')
                exists = False
                for document in listing['users']:
                    if account.username == document['user']:
                        print(f"User '{account.username}' already exists.")
                        exists = True
                if exists:
                    DBAccount.objects.filter(id=account.id).update(is_moved=True)
                else:
                    db.command('createUser', account.username, pwd=account.password, roles=[{'role': server.create_user_template, 'db': server.database}])
                    moved_accounts.append(account.username)
                    DBAccount.objects.filter(id=account.id).update(is_moved=True)
                    print(f"Successfully created user '{account.username}' with '{account.password}' password.")
            conn.close()
            return JsonResponse({'moved_accounts': moved_accounts}, status=200)
        except (Exception) as error:
            print(error)
            return JsonResponse({'name': str(error)}, status=500)
        
    def oracle(self, server, db_accounts):
        moved_accounts = []
        status_message = ''
        status_code = 500
        try:
            oracledb.init_oracle_client()
            conn = oracledb.connect(
                user=server.user,
                password=server.password,
                dsn=f"{server.host}:{server.port}/{server.database}"
            )
            cursor = conn.cursor()
            print("Successfully connected to Oracle server.")

            for account in db_accounts:
                print(account.username)
                cursor.execute(f"SELECT * FROM DBA_USERS WHERE username = '{account.username}'")
                user_exists = cursor.fetchone()
                if user_exists:
                    print(f"User '{account.username}' already exists in database.")
                    DBAccount.objects.filter(id=account.id).update(is_moved=True)
                    continue
                else:
                    cursor.execute(server.create_user_template % (account.username, account.password))
                    moved_accounts.append(account.username)
                    DBAccount.objects.filter(id=account.id).update(is_moved=True)
                    print(f"Successfully created user '{account.username}' with '{account.password}' password.")
            conn.commit()
            cursor.close()
            status_message = 'Successfully moved accounts.'
            status_code = 200
            return moved_accounts, status_message, status_code
        except (Exception) as error:
            print(error)
            status_message = str(error)
            status_code = 500
            return moved_accounts, status_message, status_code

    @action (methods=['post'], detail=False)
    def add_db_account(self, request, format=None):
        user = request.user
        if not user.has_perm('database.add_dbaccount'):
            raise PermissionDenied

        print('Request log:', request.data)

        server = Server.objects.get(id=request.data['server_id'])
        if not server.active:
            return HttpResponseBadRequest(json.dumps({'name': f"Serwer ({server.name}) nie jest aktywny."}), headers={'Content-Type': 'application/json'})

        # edition_server = EditionServer.objects.get(edition__id=request.data['edition_id'], server=server)

        # # check if all students in this group have db accounts on this server
        # students = Student.objects.filter(groups__id=request.data['group_id'])
        # for student in students:
        #     db_accounts = DBAccount.objects.filter(student=student, editionServer=edition_server)
        #     if not db_accounts:
        #         LoadStudentsFromCSV.create_db_account(student, edition_server)
        
        db_accounts = DBAccount.objects.filter(is_moved=False, editionServer__server__active=True, editionServer__server__id=request.data['server_id'], student__groups__id=request.data['group_id'])
        if not db_accounts:
            print('No accounts to move')
            server = Server.objects.get(id=request.data['server_id'])
            return HttpResponseBadRequest(json.dumps({'name': f"Wszystkie konta w grupie zostały już utworzone w zewnętrznej bazie danych ({server.name} - {server.dbms.name})."}), headers={'Content-Type': 'application/json'})

        print(f"Server: {server}, server user: {server.user}, server password: {server.password}, server ip: {server.host}, server port: {server.port}")
        
        if server.dbms.name.lower() == 'mysql' or server.dbms.name.lower() == 'my sql':  
            moved_accounts, status_message, status_code = self.mysql(server, db_accounts)
        elif server.dbms.name.lower() == 'postgres' or server.dbms.name.lower() == 'postgresql' or server.dbms.name.lower() == 'postgre sql': 
            moved_accounts, status_message, status_code = self.postgresql(server, db_accounts)
        elif server.dbms.name.lower() == 'mongo' or server.dbms.name.lower() == 'mongodb' or server.dbms.name.lower() == 'mongo db':
            moved_accounts, status_message, status_code = self.mongodb(server, db_accounts)
        elif server.dbms.name.lower() == 'oracle' or server.dbms.name.lower() == 'oracledb' or server.dbms.name.lower() == 'oracle db':
            moved_accounts, status_message, status_code = self.oracle(server, db_accounts)
        else:
            return HttpResponseBadRequest(json.dumps({'name': 'Nieznany SZBD.'}), headers={'Content-Type': 'application/json'})
        
        return JsonResponse({
                'moved_accounts': moved_accounts,
                'name': status_message}, status=status_code
            )


class RemoveUserFromExternalDB(ViewSet):
    def mysql(self, db_account):
        try:
            conn_mysql = mdb.connect(
                host=db_account.editionServer.server.host,
                port=int(db_account.editionServer.server.port),
                user=db_account.editionServer.server.user,
                passwd=db_account.editionServer.server.password,
                db=db_account.editionServer.server.database
            )
            print('Connected to MySQL server')  
            cursor = conn_mysql.cursor()
            cursor.execute(db_account.editionServer.server.delete_user_template % (db_account.username))
            conn_mysql.commit()
            DBAccount.objects.filter(id=db_account.id).update(is_moved=False)
            cursor.close()
            conn_mysql.close()
            print(f"Successfully deleted user '{db_account.username}'")
            return HttpResponse(f'deleted_account: {db_account.username}', status=200)
        except (Exception, mdb.DatabaseError) as error:
            print(error)
            return JsonResponse({'name': str(error)}, status=500)
    
    def postgresql(self, db_account):
        try:
            conn_postgres = psycopg2.connect(dbname=db_account.editionServer.server.database, user=db_account.editionServer.server.user, password=db_account.editionServer.server.password, host=db_account.editionServer.server.host, port=db_account.editionServer.server.port)
            print('Connected to Postgres server')
            cursor = conn_postgres.cursor()
            cursor.execute(db_account.editionServer.server.delete_user_template % (db_account.username))
            conn_postgres.commit()
            DBAccount.objects.filter(id=db_account.id).update(is_moved=False)
            cursor.close()
            print(f"Successfully deleted user '{db_account.username}'")
            return HttpResponse(f'deleted_account: {db_account.username}', status=200)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return JsonResponse({'name': str(error)}, status=500)

    def mongodb(self, db_account):
        try:
            conn = MongoClient(f'mongodb://{db_account.editionServer.server.user}:{db_account.editionServer.server.password}@{db_account.editionServer.server.host}:{db_account.editionServer.server.port}/')
            db = conn[db_account.editionServer.server.database]
            db.command({
                "dropUser" : db_account.username
            })
            DBAccount.objects.filter(id=db_account.id).update(is_moved=False)
            print(f"Successfully deleted user '{db_account.username}'")
            return HttpResponse(f'deleted_account: {db_account.username}', status=200)
        except (Exception, mdb.DatabaseError) as error:
            print(f"Error: {error}")
            return JsonResponse({'name': str(error)}, status=500)
    
    def oracle(self, db_account):
        try:
            oracledb.init_oracle_client()
            connection = oracledb.connect(
                user=db_account.editionServer.server.user,
                password=db_account.editionServer.server.password,
                dsn=f"{db_account.editionServer.server.host}:{db_account.editionServer.server.port}/{db_account.editionServer.server.database}")

            cursor = connection.cursor()
            # check if user exists
            cursor.execute(f"SELECT * FROM DBA_USERS WHERE username = '{db_account.username}'")
            user_exists = cursor.fetchone()
            if not user_exists:
                print(f"User '{db_account.username}' does not exist")
                DBAccount.objects.filter(id=db_account.id).update(is_moved=False)
                return HttpResponseBadRequest(json.dumps({'name': 'Użytkownik nie istnieje.'}), headers={'Content-Type': 'application/json'})

            cursor.execute(db_account.editionServer.server.delete_user_template % (db_account.username))
            connection.commit()
            DBAccount.objects.filter(id=db_account.id).update(is_moved=False)
            cursor.close()
            print(f"Successfully deleted user '{db_account.username}'")
            return HttpResponse(f'deleted_account: {db_account.username}', status=200)
        except (Exception, mdb.DatabaseError) as error:
            print(f"Error: {error}")
            return JsonResponse({'name': str(error)}, status=500)

    @action (methods=['post'], detail=False)
    def delete_db_account(self, request, format=None):
        user = request.user
        if not user.has_perm('database.remove_db_account'):
            raise PermissionDenied

        print('Request log:', request.data)
        db_account = DBAccount.objects.get(id=request.data['dbaccount_id'])
        db_account_server_provider = db_account.editionServer.server.dbms.name
        
        if db_account_server_provider.lower() == 'mysql':
            return self.mysql(db_account)
        elif db_account_server_provider.lower() == 'postgres' or db_account_server_provider.lower() == 'postgresql':
            return self.postgresql(db_account)
        elif db_account_server_provider.lower() == 'mongo' or db_account_server_provider.lower() == 'mongodb':
            return self.mongodb(db_account)
        elif db_account_server_provider.lower() == 'oracle' or db_account_server_provider.lower() == 'oracledb':
            return self.oracle(db_account)
        else:
            return HttpResponseBadRequest(json.dumps({'name': 'Nieznany SZBD.'}), headers={'Content-Type': 'application/json'})


class LoadStudentsFromCSV(ViewSet):
    def read_csv(self, user, data):
        status_message = ''
        status_code = 200
        students_list = []

        if 'group_id' not in data or 'students_csv' not in data:
            print('Error: group_id or students_csv not found in request data.')
            status_message = 'Nie podano grupy lub pliku.'
            status_code = 400
            return students_list, status_message, status_code

        try:
            students_csv = data['students_csv'].read().decode('utf-8-sig')
            csv_reader = csv.DictReader(students_csv.splitlines(), delimiter=',')
            students_list = list(csv_reader)
            # print('students_list: ', students_list)
        except Exception as error:
            print('Błędny plik csv.', error)
            status_message = 'Błąd podczas wczytywania pliku csv. Upewnij się czy próbujesz przesłać poprawny plik (z kodowaniem UTF-8).'
            status_code = 400
            return students_list, status_message, status_code

        if 'first_name' not in students_list[0] or 'last_name' not in students_list[0] or 'email' not in students_list[0] or 'student_id' not in students_list[0]:
            print("Bad request. Błędny plik csv.")
            status_message = 'Błąd podczas wczytywania pliku csv. Upewnij się, że zawiera on następujące kolumny: first_name, last_name, email i student_id.'
            status_code = 400
            return students_list, status_message, status_code

        # checking if all columns have appropriate values
        for student in students_list:
            if student['first_name'] is None or student['last_name'] is None or student['email'] is None or student['student_id'] is None:
                print("Błąd podczas wczytywania pliku csv. Nie wszystkie kolumny zawierają wartości.")
                status_message = 'Błąd podczas wczytywania pliku csv. Nie wszystkie kolumny zawierają wartości.'
                status_code = 400
                return students_list, status_message, status_code
            if not user._validate_email(student['email']):
                print("Błąd podczas wczytywania pliku csv. Niepoprawny email.")
                status_message = 'Błąd podczas wczytywania pliku csv. Niepoprawny email.'
                status_code = 400
                return students_list, status_message, status_code

        return students_list, status_message, status_code

    def get_username(self, added_student, edition_server):
        return edition_server.server.username_template.lower().replace(
            r'{imie}', added_student.user.first_name.lower()).replace(
            r'{imię}', added_student.user.first_name.lower()).replace(
            r'{nazwisko}', added_student.user.last_name.lower()).replace(
            r'{nr_indeksu}', added_student.student_id.lower()).replace(
            r'{numer_indeksu}', added_student.student_id.lower()).replace(
            r'{nr_ind}', added_student.student_id.lower()).replace(
            r'{indeks}', added_student.student_id.lower()).replace(
            r'{email}', added_student.user.email.lower()
        )
    
    def create_db_account(self, student, edition_server):
        username_to_add = self.get_username(student, edition_server)
        if DBAccount.objects.filter(username=username_to_add, editionServer=edition_server).exists():
            # print(f"Account {added_account.username} on {added_account.editionServer.server.name} ({added_account.editionServer.server.dbms.name}) server already exists.")
            created = False
        else:
            DBAccount.objects.create(
                username=username_to_add, password=User.objects.make_random_password(length=10), student=student, editionServer=edition_server
            )
            # print(f"Added {added_account.username} on {added_account.editionServer.server.name} ({added_account.editionServer.server.dbms.name}) server.")
            created = True
        return created


    @action (methods=['post'], detail=False)
    def load_students_csv(self, request, format=None):
        user = request.user
        if not user.has_perm('database.load_from_csv'):
            raise PermissionDenied

        print('Request log:', request.data)

        students_list, status_message, status_code = self.read_csv(user, request.data)
        if status_message != '' or status_code != 200:
            return JsonResponse({'name': status_message}, status=status_code)
        
        group_id = request.data['group_id']
        students_info = []

        try:
            # print(group_id)
            group_to_add = Group.objects.get(id=group_id)
            print(f'Group to add: {group_to_add.name}')
            # if group_to_add is None:
            #     print('Group not found.')
            #     return HttpResponseBadRequest(json.dumps({'name': 'Grupa nie została znaleziona.'}), headers={'Content-Type': 'application/json'})
        except Exception as error:
            print(error)
            return HttpResponseBadRequest(json.dumps({'name': 'Nie znaleziono grupy.'}), headers={'Content-Type': 'application/json'})

        available_edition_servers = EditionServer.objects.filter(edition__teacheredition__groups=group_to_add.id)
        if len(available_edition_servers) == 0:
            print("No available edition servers.")
            return HttpResponseBadRequest(json.dumps({'name': 'Brak serwera w danej edycji'}), headers={'Content-Type': 'application/json'})

        try:
            for student in students_list:
                students_info.append({
                    'first_name': student['first_name'],
                    'last_name': student['last_name'],
                    'email': student['email'], 
                    'student_id': student['student_id'],
                    'student_created': '',
                    'added_to_group': '',
                    'account_created': {f"{editionServer.server.name} ({editionServer.server.dbms.name})": {} for editionServer in available_edition_servers}
                })
                student_info_index = next((i for i, student_info in enumerate(students_info) if student_info['student_id'] == student['student_id']), None)
                if Student.objects.filter(student_id=student['student_id']).exists():
                    added_student = Student.objects.get(student_id=student['student_id'])
                    # added_user = added_student.user
                    students_info[student_info_index]['student_created'] = False
                    # print(f"Student {added_student.user.first_name} {added_student.user.last_name} - {added_student.student_id} already exists.")
                else:
                    added_user = User.objects.create_user(
                        first_name=student['first_name'],
                        last_name=student['last_name'],
                        email=student['email'],
                        password=User.objects.make_random_password(length=10),
                        is_active=True,
                        is_student=True
                    )

                    added_student = Student.objects.create(
                        user=added_user,
                        student_id=student['student_id']
                    )

                    students_info[student_info_index]['student_created'] = True
                    # print(f"Student {added_user.first_name} {added_user.last_name} created.")

                if added_student in group_to_add.students.all():
                    # print(f"Student {added_user.first_name} {added_user.last_name} already exists in group {group_to_add.name}.")
                    students_info[student_info_index]['added_to_group'] = False
                else:
                    group_to_add.students.add(added_student)
                    # print(f"Student {added_user.first_name} {added_user.last_name} added to group {group_to_add.name}.")
                    students_info[student_info_index]['added_to_group'] = True

                for edition_server in available_edition_servers:
                    created = self.create_db_account(added_student, edition_server)
                    students_info[student_info_index]['account_created'][f"{edition_server.server.name} ({edition_server.server.dbms.name})"] = created            
            
            group_to_add.save()

        except Exception as error:
            print(f"Error: {error}")
            return JsonResponse({"name": str(error), "students_info": students_info}, status=500)
            
        return JsonResponse({"students_info": students_info}, status=200)


class ChangeActiveSemester(ViewSet):
    @action (methods=['post'], detail=False)
    def change_active_semester(self, request, format=None):
        user = request.user
        if not user.has_perm('database.change_active_semester'):
            raise PermissionDenied

        data = request.data
        print('Request log:', data)

        if 'semester_id' not in data:
            print('Error: semester_id not found in request data.')
            return HttpResponseBadRequest(json.dumps({'name': 'Nie podano semestru.'}), headers={'Content-Type': 'application/json'})
        semester_id = data['semester_id']

        try:
            semester_to_change = Semester.objects.get(id=semester_id)
            if semester_to_change.active:
                print('Semester is already active.')
                return HttpResponseBadRequest(json.dumps({'name': 'Semestr jest już aktywny.'}), headers={'Content-Type': 'application/json'})
            Semester.objects.update(active=False)
            semester_to_change.active = True
            semester_to_change.save()
            return HttpResponse(status=200)
        except Exception as error:
            print(error)
            return JsonResponse({'name': str(error)}, status=500)


class AddStudentsToGroup(ViewSet):
    @action (methods=['post'], detail=False)
    def add_students_to_group(self, request, format=None):
        user = request.user
        if not user.has_perm('database.add_students_to_group'):
            raise PermissionDenied

        data = request.data
        print('Request log:', data)
        group_id = data['group_id']
        students = data['students']

        added_students = []
        added_accounts = []

        if 'group_id' not in data:
            print('Error: group_id not found in request data.')
            return HttpResponseBadRequest(json.dumps({'name': 'Nie podano grupy.'}), headers={'Content-Type': 'application/json'})

        if 'students' not in data:
            print('Error: students not found in request data.')
            return HttpResponseBadRequest(json.dumps({'name': 'Nie podano studentów.'}), headers={'Content-Type': 'application/json'})
        
        try:
            group_to_add = Group.objects.get(id=group_id)
        except Exception as error:
            print(error)
            return HttpResponseBadRequest(json.dumps({'name': 'Grupa o takim ID nie istnieje'}), headers={'Content-Type': 'application/json'})

        try:
            available_edition_servers = EditionServer.objects.filter(edition__teacheredition__groups=group_to_add.id)
            print(available_edition_servers)
        except Exception as error:
            print(error)
            return HttpResponseBadRequest(json.dumps({'name': 'Nie znaleziono serwera dla danej edycji'}), headers={'Content-Type': 'application/json'})
        
        if len(available_edition_servers) == 0:
            print("No available edition servers.")
            return HttpResponseBadRequest(json.dumps({'name': 'Brak serwera w danej edycji'}), headers={'Content-Type': 'application/json'})

        try:
            for student_id in students:
                student_to_add = Student.objects.get(id=student_id)
                if student_to_add in group_to_add.students.all():
                    print(f"Student {student_to_add.user.first_name} {student_to_add.user.last_name} already exists in group {group_to_add.name}.")
                else:
                    group_to_add.students.add(student_to_add)
                    print(f"Student {student_to_add.user.first_name} {student_to_add.user.last_name} added to group {group_to_add.name}.")
                    added_students.append(F"{student_to_add.user.first_name} {student_to_add.user.last_name} - {student_to_add.student_id}")

                for edition_server in available_edition_servers:
                    username_to_add = edition_server.server.username_template.lower().replace(
                        r'{imie}', student_to_add.user.first_name.lower()).replace(
                        r'{imię}', student_to_add.user.first_name.lower()).replace(
                        r'{nazwisko}', student_to_add.user.last_name.lower()).replace(
                        r'{nr_indeksu}', student_to_add.student_id.lower()).replace(
                        r'{numer_indeksu}', student_to_add.student_id.lower()).replace(
                        r'{nr_ind}', student_to_add.student_id.lower()).replace(
                        r'{indeks}', student_to_add.student_id.lower()).replace(
                        r'{email}', student_to_add.user.email.lower()
                    )

                    if DBAccount.objects.filter(student=student_to_add, editionServer__server=edition_server.server).exists():
                        added_account = DBAccount.objects.get(student=student_to_add, editionServer__server=edition_server.server)
                        print(added_account)
                        print(f"Account {added_account.username} on {added_account.editionServer.server.name} ({added_account.editionServer.server.dbms.name}) server already exists.")
                        print("After if, before else")
                    else:
                        print("After else, before create")
                        if not DBAccount.objects.filter(username=username_to_add, editionServer=edition_server).exists():
                            added_account = DBAccount.objects.create(
                                username=username_to_add, password=User.objects.make_random_password(), student=student_to_add, editionServer=edition_server, is_moved=False
                            )
                            print("After create")
                            added_accounts.append(added_account.username)
                            print(f"Added {added_account.username} on {added_account.editionServer.server.name} ({added_account.editionServer.server.dbms.name}) server.")                
            
            print("before save")
            group_to_add.save()
            print('Added students: ', added_students)
            print('Added accounts: ', added_accounts)

            return JsonResponse({
                'added_students': added_students,
                'added_accounts': added_accounts
                }, status=200)

        except Exception as error:
            print(error)
            return JsonResponse({'name': str(error)}, status=500)


class RemoveStudentFromGroup(ViewSet):
    @action (methods=['post'], detail=False)
    def remove_student_from_group(self, request, format=None):
        user = request.user
        if not user.has_perm('database.remove_student_from_group'):
            raise PermissionDenied

        data = request.data
        print('Request log:', data)

        if 'group_id' not in data:
            print('Error: group_id not found in request data.')
            return HttpResponseBadRequest(json.dumps({'name': 'Nie podano grupy.'}), headers={'Content-Type': 'application/json'})

        if 'student_id' not in data:
            print('Error: students not found in request data.')
            return HttpResponseBadRequest(json.dumps({'name': 'Nie podano studenta.'}), headers={'Content-Type': 'application/json'})

        group_id = data['group_id']
        student_id = data['student_id']

        try:
            group_to_remove = Group.objects.get(id=group_id)
        except Exception as error:
            print(error)
            return HttpResponseBadRequest(json.dumps({'name': 'Grupa o takim ID nie istnieje.'}), headers={'Content-Type': 'application/json'})

        try:
            student_to_remove = Student.objects.get(id=student_id)
            if student_to_remove in group_to_remove.students.all():
                group_to_remove.students.remove(student_to_remove)
                group_to_remove.save()
                print(f"Student {student_to_remove.first_name} {student_to_remove.last_name} removed from group {group_to_remove.name}.")
                return JsonResponse({'removed student: ': student_to_remove.student_id}, status=200)
            else:
                print(f"Student {student_to_remove.first_name} {student_to_remove.last_name} does not exist in group {group_to_remove.name}.")
                return HttpResponseBadRequest(json.dumps({'name': 'Student nie należy do tej grupy.'}), headers={'Content-Type': 'application/json'})
        except Exception as error:
            print(error)
            return JsonResponse({'name': str(error)}, status=500)

class ResetOwnPassword(ViewSet):
    @action (methods=['post'], detail=False)
    def reset_own_password(self, request, format=None):
        user = request.user
        if not user.has_perm('database.reset_own_password'):
            raise PermissionDenied

        try:
            account_to_reset = User.objects.get(id=user.id)
            new_password = User.objects.make_random_password()
            print(f"New password for {account_to_reset.email} is {new_password}.")
            account_to_reset.set_password(new_password)
            account_to_reset.save()
            user.send_email_gmail(RESET_PASSWORD_SUBJECT, RESET_PASSWORD_MESSAGE, new_password)
            logout(request)
            return JsonResponse({'name': "Succesfull password reset for " + str(account_to_reset.email)}, status=200)
        except Exception as error:
            print(error)
            return JsonResponse({'name': str(error)}, status=500)
                

class ResetStudentPassword(ViewSet):
        @action (methods=['post'], detail=False)
        def reset_student_password(self, request, format=None):
            user = request.user
            if not user.has_perm('database.reset_student_password'):
                raise PermissionDenied
    
            data = request.data
            print('Request log:', data)
    
            if 'account_id' not in data:
                print('Error: account_id not found in request data.')
                return HttpResponseBadRequest(json.dumps({'name': 'Nie podano konta.'}), headers={'Content-Type': 'application/json'})
    
            account_id = data['account_id']
    
            try:
                account_to_reset = User.objects.get(id=account_id)
                new_password = User.objects.make_random_password()
                print(f"New password for {account_to_reset.email} is {new_password}.")
                account_to_reset.set_password(new_password)
                account_to_reset.save()
                user.send_email_gmail(RESET_PASSWORD_SUBJECT, RESET_PASSWORD_MESSAGE, new_password)
                return JsonResponse({'name': "Succesfull password reset for " + str(account_to_reset.email)}, status=200)
            except Exception as error:
                print(error)
                return JsonResponse({'name': str(error)}, status=500)

class UpdatePasswordAfterReset(ViewSet):

    @action (methods=['post'], detail=False)
    def update_password_after_reset(self, request, format=None):
        user = request.user
        if not user.has_perm('database.update_password_after_reset'):
            raise PermissionDenied

        data = request.data

        if 'current_password' not in data:
            print('Error: current_password not found in request data.')
            return HttpResponseBadRequest(json.dumps({'name': 'Nie podano hasła.'}), headers={'Content-Type': 'application/json'})

        if 'new_password' not in data:
            print('Error: new_password not found in request data.')
            return HttpResponseBadRequest(json.dumps({'name': 'Nie podano nowego hasła.'}), headers={'Content-Type': 'application/json'})
       
        old_password = data['current_password']
        new_password = data['new_password']

        try:
            account_to_update = User.objects.get(id=user.id)
            # hash the old_password variable so it matches the hash in the database
            if check_password(old_password, account_to_update.password):
                account_to_update.set_password(new_password)
                account_to_update.save()
                print(f"Password updated for {account_to_update.email}")
                logout(request)
                return JsonResponse({'name': "Succesfull password update for account of id: " + str(account_to_update.id)}, status=200)
            else:
                print(f"Wrong password for {account_to_update.email}")
                return HttpResponseBadRequest(json.dumps({'name': 'Niepoprawne hasło.'}), headers={'Content-Type': 'application/json'})
        except Exception as error:
            print(error)
            return JsonResponse({'name': str(error)}, status=500)


class ResetDBPassword(ViewSet):
    @action (methods=['post'], detail=False)
    def reset_db_password(self, request, format=None):
        user = request.user
        if not user.has_perm('database.reset_db_password'):
            raise PermissionDenied

        data = request.data

        if 'dbaccount_id' not in data:
            print('Error: dbaccount_id not found in request data.')
            return HttpResponseBadRequest(json.dumps({'name': 'Nie podano konta.'}), headers={'Content-Type': 'application/json'})
        dbaccount_id = data['dbaccount_id']

        if user.is_student:
            try:
                account_to_reset = DBAccount.objects.get(id=dbaccount_id)
                if account_to_reset.student.user.id != user.id:
                    print('Error: student tried to reset password for account that is not his own.')
                    return HttpResponseBadRequest(json.dumps({'name': 'Nie możesz zresetować hasła dla konta, które nie jest Twoje.'}), headers={'Content-Type': 'application/json'})
            except Exception as error:
                print(error)
                return JsonResponse({'name': str(error)}, status=500)

        if user.is_teacher:
            try:
                account_to_reset = DBAccount.objects.get(id=dbaccount_id)
                teacher = Teacher.objects.get(user=user)
                groups = Group.objects.filter(teacherEdition__teacher=teacher)
                students = Student.objects.filter(groups__teacherEdition__teacher=teacher).prefetch_related(Prefetch('groups', queryset=groups))
                if account_to_reset.student not in students:
                    print('Error: teacher tried to reset password for account that is not his student.')
                    return HttpResponseBadRequest(json.dumps({'name': 'Nie możesz zresetować hasła dla konta, które nie należy do studenta z twojej grupy.'}), headers={'Content-Type': 'application/json'})
            except Exception as error:
                print(error)
                return JsonResponse({'name': str(error)}, status=500)

        try:
            account_to_reset = DBAccount.objects.get(id=dbaccount_id)
            new_password = User.objects.make_random_password(length=10)
            account_to_reset.password = new_password
            account_to_reset.save()

            server = Server.objects.get(id=account_to_reset.editionServer.server.id)
            db_account_server_provider = server.dbms.name

            if db_account_server_provider == 'MySQL':
                conn_mysql = mdb.connect(host=server.host, port=int(server.port), user=server.user, passwd=server.password, db=server.database)
                cursor = conn_mysql.cursor()
                cursor.execute(server.modify_user_template % (account_to_reset.username, new_password))
                conn_mysql.commit()
                conn_mysql.close()
            
            elif db_account_server_provider == 'PostgreSQL':
                conn_postgres = psycopg2.connect(host=server.host, port=server.port, user=server.user, password=server.password, database=server.database)
                cursor = conn_postgres.cursor()
                cursor.execute(server.modify_user_template % (account_to_reset.username, new_password))
                conn_postgres.commit()
                conn_postgres.close()
            
            elif db_account_server_provider == 'Oracle':
                oracledb.init_oracle_client()
                conn = oracledb.connect(
                    user=server.user,
                    password=server.password,
                    dsn=f"{server.host}:{server.port}/{server.database}")
                cursor = conn.cursor()
                cursor.execute(server.modify_user_template % (account_to_reset.username, new_password))
                conn.commit()
                conn.close()
            elif db_account_server_provider == 'MongoDB':
                conn = MongoClient(f'mongodb://{server.user}:{server.password}@{server.host}:{server.port}/')
                db = conn[server.database]
                db.command("updateUser", account_to_reset.username, pwd=new_password)
                conn.close()
            else:
                print('Error: Unknown server provider.')
                return HttpResponseBadRequest(json.dumps({'name': 'Nieznany SZBD.'}), headers={'Content-Type': 'application/json'})

            print("Password reseted for account: ", account_to_reset.username)
            return JsonResponse({'name': "Succesfull password reset for account of id: " + str(account_to_reset.id)}, status=200)
        except Exception as error:
            print(error)
            return JsonResponse({'name': str(error)}, status=500)


class DeleteEdition(ViewSet):
    @action (methods=['post'], detail=False)
    def delete_edition(self, request, format=None):
        user = request.user
        if not user.has_perm('database.delete_edition'):
            raise PermissionDenied

        data = request.data

        if 'edition_id' not in data:
            print('Error: edition_id not found in request data.')
            return HttpResponseBadRequest(json.dumps({'name': 'Nie podano edycji.'}), headers={'Content-Type': 'application/json'})
        edition_id = data['edition_id']

        try:
            edition_to_delete = Edition.objects.get(id=edition_id)
            edition_to_delete.delete()
            print("Edition deleted: ", edition_to_delete.id)
            return JsonResponse({'name': "Succesfull edition delete of id: " + str(edition_to_delete.id)}, status=200)
        except Exception as error:
            print(error)
            return JsonResponse({'name': str(error)}, status=500)

# endpoint to delete students and their user with no groups
class DeleteStudentsWithoutGroups(ViewSet):
    @action (methods=['post'], detail=False)
    def delete_students_without_groups(self, request, format=None):
        user = request.user
        if not user.has_perm('database.delete_student'):
            raise PermissionDenied

        try:
            students_to_delete = Student.objects.filter(groups__isnull=True)
            if students_to_delete.count() == 0:
                return HttpResponseBadRequest(json.dumps({'name': 'Brak studentów do usunięcia.'}), headers={'Content-Type': 'application/json'})

            for student in students_to_delete:
                print(student)
                student.user.delete()
                # student.delete()
            print("Students deleted: ", students_to_delete)
            return JsonResponse({
                'name': "Pomyślnie usunięto studentów",
                # 'students': [student.email for student in students_to_delete]
            }, status=200)
        except Exception as error:
            print(error)
            return JsonResponse({'name': str(error)}, status=500)