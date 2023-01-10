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
from django.core.validators import validate_email
import json

from database.password_generator import PasswordGenerator
from database.sender import EmailSender
from .serializers import UserSerializer, TeacherSerializer, DetailedTeacherSerializer, StudentSerializer, DetailedStudentSerializer, MajorSerializer, CourseSerializer, SemesterSerializer, BasicSemesterSerializer, EditionSerializer, BasicEditionSerializer, TeacherEditionSerializer, GroupSerializer, DetailedGroupSerializer, GroupSerializerForStudent, ServerSerializer, EditionServerSerializer, DBAccountSerializer
# , SimpleTeacherEditionSerializer
from .models import User, Teacher, Student, Major, Course, Semester, Edition, TeacherEdition, Group, Server, EditionServer, DBAccount

INVALID_EMAIL = 'Niepoprawny adres email.'
EMAIL_DUPLICATED = 'Podany adres email jest już zajęty.'
MISSING_FIELDS = 'Nie podano wszystkich wymaganych pól.'

def email_validation(email):
    try:
        validate_email(email)
        # print("Valid email address.")
    except ValidationError:
        # print("Bad request. Błędny adres email.")
        return False
    return True


class UserViewSet(ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting users.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'password', 'email', 'first_name', 'last_name', 'is_student', 'is_teacher', 'is_staff', 'is_superuser', 'is_active']

    def get_queryset(self):
        user = self.request.user

        if not user.has_perm('database.view_user'):
            raise PermissionDenied

        if user.is_superuser:
            return User.objects.all()
        return User.objects.filter(id=user.id)

    def create(self, request, *args, **kwargs):
        user = request.user
        if not user.has_perm('database.add_user'):
            raise PermissionDenied()
        # create superuser
        if not user.is_superuser:
            raise PermissionDenied()
        
        if not email_validation(request.data['email']):
            return JsonResponse({'name': INVALID_EMAIL}, status=400)

        new_superuser = User.objects.create_superuser(
            email=request.data['email'],
            # password=PasswordGenerator(10).generate_password(),
            password='admin',
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
            if not email_validation(request.data['email']):
                return JsonResponse({'name': INVALID_EMAIL}, status=400)
            try:
                # new_password = PasswordGenerator(10).generate_password()
                new_password = 'password'
                user = User.objects.create_user(
                    email=request.data['email'],
                    first_name=request.data['first_name'],
                    last_name=request.data['last_name'],
                    password = new_password,
                    is_teacher=True,
                )
                TeacherViewSet.grant_teacher_permissions(self, user)
                teacher = Teacher.objects.create(user=user)
                email_sender = EmailSender()
                email_sender.send_email_gmail("putdb2023@gmail.com", new_password)
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
            # student = Student.objects.get(user=user)
            # groups = Group.objects.filter(students=student).prefetch_related(Prefetch('students', queryset=Student.objects.filter(user=user)))
            # return groups.order_by('id').distinct()
        elif user.is_student:
            # student = get_object_or_404(Student, user=user)
            return Student.objects.filter(user=user)
        else:
            return Student.objects.none()

    # def retrieve(self, request, *args, **kwargs):
    #     user = request.user

    #     if not user.has_perm('database.view_student'):
    #         raise PermissionDenied

    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     groups = instance.groups.all()
    #     db_accounts = instance.db_accounts.all()
    #     resp = serializer.data
    #     resp['groups'] = GroupSerializerForStudent(groups, many=True).data
    #     resp['db_accounts'] = DBAccountSerializer(db_accounts, many=True).data
    #     return Response(resp, status=200)

    def create(self, request, *args, **kwargs):
        user = request.user
        if not user.has_perm('database.add_student'):
            raise PermissionDenied()
        
        # check if request.data contains fields from user model
        if 'email' in request.data and 'first_name' in request.data and 'last_name' in request.data and 'student_id' in request.data and 'major' in request.data:
            if not email_validation(request.data['email']):
                return JsonResponse({'name': INVALID_EMAIL}, status=400)
            try:
                # new_password = PasswordGenerator(10).generate_password()
                new_password = 'password'
                user = User.objects.create_user(
                    email=request.data['email'],
                    first_name=request.data['first_name'],
                    last_name=request.data['last_name'],
                    password=new_password,
                    is_student=True,
                )
                StudentViewSet.grant_student_permissions(self, user)
                major = Major.objects.get(id=request.data['major'])
                student = Student.objects.create(user=user, student_id=request.data['student_id'], major=major)
                email_sender = EmailSender()
                email_sender.send_email_gmail("putdb2023@gmail.com", new_password)
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
        student.delete()
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
            print("destroy")
            teacher_editions = TeacherEdition.objects.filter(edition=self.get_object().id)
            if teacher_editions.exists():
                for teacher_edition in teacher_editions:
                    if Group.objects.filter(teacherEdition=teacher_edition).exists():
                        return HttpResponseBadRequest(json.dumps({'name': 'Edycja ma przypisane grupy.'}), headers={'Content-Type': 'application/json'})
            edition = Edition.objects.get(id=self.get_object().id)
            # serializer = EditionSerializer(edition)
            print("Callind delete...")
            edition.delete()
            print("Deleted!")
            # return Response(serializer.data, status=204)
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

        return super().get_queryset()

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



# class SimpleTeacherEditionViewSet(ModelViewSet):
#     """
#     A simple ViewSet for listing, retrieving and posting teachers in editions.
#     """
#     serializer_class = SimpleTeacherEditionSerializer
#     queryset = TeacherEdition.objects.select_related('teacher').only('id', 'teacher_id')
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = [
#         'id',
#         'teacher',
#         'teacher__user',
#         'teacher__user__first_name',
#         'teacher__user__last_name',
#         'edition',
#     ]


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
        'teacherEdition__edition__servers__ip',
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

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        all_accounts_moved = True

        if not user.is_student:
            for student in instance.students.all():
                for db_account in student.db_accounts.all():
                    if db_account.is_moved == False:
                        all_accounts_moved = False
                        break
                if all_accounts_moved == False:
                    break
        resp = serializer.data
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
            student = Student.objects.get(user=user)
            groups = Group.objects.filter(students=student).prefetch_related(Prefetch('students', queryset=student))
            return groups.order_by('id').distinct()
        else:
            return Group.objects.none()


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
        'ip', 
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
    @action (methods=['post'], detail=False)
    def add_db_account(self, request, format=None):

        user = request.user
        if not user.has_perm('database.add_dbaccount'):
            raise PermissionDenied

        accounts_data = request.data
        print('Request log:', accounts_data)

        server = Server.objects.get(id=accounts_data['server_id'])
        if not server.active:
            return HttpResponseBadRequest(json.dumps({'name': f"Serwer ({server.name}) nie jest aktywny."}), headers={'Content-Type': 'application/json'})

        db_accounts = DBAccount.objects.filter(is_moved=False, editionServer__server__active=True, editionServer__server__id=accounts_data['server_id'], student__groups__id=accounts_data['group_id'])

        if not db_accounts:
            print('No accounts to move')
            server = Server.objects.get(id=accounts_data['server_id'])
            return HttpResponseBadRequest(json.dumps({'name': f"Wszystkie konta w grupie zostały już utworzone w zewnętrznej bazie danych ({server.name} - {server.provider})."}), headers={'Content-Type': 'application/json'})

        # server = Server.objects.get(id=accounts_data['server_id'], active=True)
        moved_accounts = []

        print(f"Server: {server}, server user: {server.user}, server password: {server.password}, server ip: {server.ip}, server port: {server.port}")
        
        if server.provider.lower() == 'mysql':  
            try:
                conn_mysql = mdb.connect(host=server.ip, port=int(server.port), user=server.user, passwd=server.password, db=server.database)
                print('Connected to MySQL server')
                cursor = conn_mysql.cursor()
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
                    return HttpResponseBadRequest(json.dumps({'name': f"Nie udało się połączyć z serwerem baz danych ({server.name} - {server.provider})."}), headers={'Content-Type': 'application/json'})
                return HttpResponseServerError(json.dumps({'name': str(error)}), headers={'Content-Type': 'application/json'})

            # connect to mysql server using odbc driver

            # try:
            #     conn_mysql = pyodbc.connect(f"DRIVER={server.driver};SERVER={server.ip};PORT={server.port};DATABASE={server.database};USER={server.user};PASSWORD={server.password}")
            #     print('Connected to MySQL server')
            #     cursor = conn_mysql.cursor()
            #     for account in db_accounts:
            #         print(server.create_user_template)
            #         cursor.execute(server.create_user_template % (account.username, account.password))
            #         moved_accounts.append(account.username)
            #         DBAccount.objects.filter(id=account.id).update(is_moved=True)
            #         print(f"Successfully created user '{account.username}' with '{account.password}' password.")
            #     conn_mysql.commit()
            #     cursor.close()
            #     conn_mysql.close()

            #     return JsonResponse({'moved_accounts': moved_accounts}, status=200)

            # except (Exception, pyodbc.DatabaseError) as error:
            #     print("error: ", error)
            #     return HttpResponse(error, status=500)
                

        elif server.provider.lower() == 'postgres' or server.provider.lower() == 'postgresql': 
            try:
                conn_postgres = psycopg2.connect(dbname=server.database, user=server.user, password=server.password, host=server.ip, port=server.port)
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
                    return HttpResponseBadRequest(json.dumps({'name': f"Nie udało się połączyć z serwerem baz danych ({server.name} - {server.provider})."}), headers={'Content-Type': 'application/json'})
                return HttpResponseServerError(json.dumps({'name': str(error)}), headers={'Content-Type': 'application/json'})

        elif server.provider.lower() == 'mongo' or server.provider.lower() == 'mongodb':
            try:
                conn = MongoClient(f'mongodb://{server.user}:{server.password}@{server.ip}:{server.port}/')
                db = conn[server.database]
                for account in db_accounts:
                    print(account.username)

                    listing = db.command('usersInfo')
                    exists = False
                    for document in listing['users']:
                        if account.username == document['user']:
                            print(f"User '{account.username}' already exists.")
                            exists = True

                    if exists:
                        DBAccount.objects.filter(id=account.id).update(is_moved=True)
                    else:
                        db.command('createUser', account.username, pwd=account.password, roles=[{'role': 'readWrite', 'db': server.database}])
                        moved_accounts.append(account.username)
                        DBAccount.objects.filter(id=account.id).update(is_moved=True)
                        print(f"Successfully created user '{account.username}' with '{account.password}' password.")
                conn.close()
                return JsonResponse({'moved_accounts': moved_accounts}, status=200)
            except (Exception) as error:
                print(error)
                return HttpResponseServerError(json.dumps({'name': str(error)}), headers={'Content-Type': 'application/json'})

        elif server.provider.lower() == 'oracle' or server.provider.lower() == 'oracledb':
            try:
                oracledb.init_oracle_client()

                conn = oracledb.connect(
                    user=server.user,
                    password=server.password,
                    dsn=f"{server.ip}:{server.port}/{server.database}")

                print("Successfully connected to Oracle server.")

                cursor = conn.cursor()
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
                return Response(json.dumps({
                    'moved_accounts': moved_accounts
                }), headers={'Content-Type': 'application/json'}, status=200)
            except (Exception) as error:
                print(error)
                return HttpResponseServerError(json.dumps({'name': str(error)}), headers={'Content-Type': 'application/json'})
        else:
            return HttpResponseBadRequest(json.dumps({'name': 'Nieznany SZBD.'}), headers={'Content-Type': 'application/json'})


class RemoveUserFromExternalDB(ViewSet):
    @action (methods=['post'], detail=False)
    def delete_db_account(self, request, format=None):

        user = request.user
        if not user.has_perm('db_accounts.move_db_account'):
            raise PermissionDenied

        accounts_data = request.data
        print('Request log:', accounts_data)

        db_account = DBAccount.objects.get(id=accounts_data['dbaccount_id'])
        db_account_server_provider = db_account.editionServer.server.provider
        
        if db_account_server_provider.lower() == 'mysql':
            try:
                conn_mysql = mdb.connect(host=db_account.editionServer.server.ip, port=int(db_account.editionServer.server.port), user=db_account.editionServer.server.user, passwd=db_account.editionServer.server.password, db=db_account.editionServer.server.database)
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
                return HttpResponseServerError(json.dumps({'name': str(error)}), headers={'Content-Type': 'application/json'})
                
        elif db_account_server_provider.lower() == 'postgres' or db_account_server_provider.lower() == 'postgresql':
            try:
                conn_postgres = psycopg2.connect(dbname=db_account.editionServer.server.database, user=db_account.editionServer.server.user, password=db_account.editionServer.server.password, host=db_account.editionServer.server.ip, port=db_account.editionServer.server.port)
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
                return HttpResponseServerError(json.dumps({'name': str(error)}), headers={'Content-Type': 'application/json'})

        elif db_account_server_provider.lower() == 'mongo' or db_account_server_provider.lower() == 'mongodb':
            try:
                conn = MongoClient(f'mongodb://{db_account.editionServer.server.user}:{db_account.editionServer.server.password}@{db_account.editionServer.server.ip}:{db_account.editionServer.server.port}/')
                db = conn[db_account.editionServer.server.database]
                db.command({
                    "dropUser" : db_account.username
                })
                DBAccount.objects.filter(id=db_account.id).update(is_moved=False)
                print(f"Successfully deleted user '{db_account.username}'")
                return HttpResponse(f'deleted_account: {db_account.username}', status=200)
            except (Exception, mdb.DatabaseError) as error:
                print(f"Error: {error}")
                return HttpResponseServerError(json.dumps({'name': str(error)}), headers={'Content-Type': 'application/json'})
        elif db_account_server_provider.lower() == 'oracle' or db_account_server_provider.lower() == 'oracledb':
            try:
                oracledb.init_oracle_client()

                connection = oracledb.connect(
                    user=db_account.editionServer.server.user,
                    password=db_account.editionServer.server.password,
                    dsn=f"{db_account.editionServer.server.ip}:{db_account.editionServer.server.port}/{db_account.editionServer.server.database}")

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
                return HttpResponseServerError(json.dumps({'name': str(error)}), headers={'Content-Type': 'application/json'})

        
        return HttpResponseBadRequest(json.dumps({'name': 'Nieznany SZBD.'}), headers={'Content-Type': 'application/json'})


class LoadStudentsFromCSV(ViewSet):

    @action (methods=['post'], detail=False)
    def load_students_csv(self, request, format=None):

        user = request.user
        if not user.has_perm('database.load_from_csv'):
            raise PermissionDenied

        accounts_data = request.data
        print('Request log:', accounts_data)

        if 'group_id' not in accounts_data or 'students_csv' not in accounts_data:
            print('Error: group_id or students_csv not found in request data.')
            return HttpResponseBadRequest(json.dumps({'name': 'Nie podano grupy lub pliku.'}))
            
        group_id = accounts_data['group_id']
        students_csv = accounts_data['students_csv']

        try:
            students_csv = students_csv.read().decode('utf-8-sig')
            csv_reader = csv.DictReader(students_csv.splitlines(), delimiter=',')
            students_list = list(csv_reader)
            print('students_list: ', students_list)
        except Exception as error:
            print('Błędny plik csv.', error)
            return HttpResponseNotFound(json.dumps({'name': 'Błąd podczas wczytywania pliku csv. Upewnij się czy próbujesz przesłać poprawny plik (z kodowaniem UTF-8).'}), headers={'Content-Type': 'application/json'})

        students_info = []

        if 'first_name' not in students_list[0] or 'last_name' not in students_list[0] or 'email' not in students_list[0] or 'student_id' not in students_list[0]:
            print("Bad request. Błędny plik csv.")
            return HttpResponseBadRequest(json.dumps({'name': 'Błędny plik csv. Upewnij się, że zawiera on następujące kolumny: first_name, last_name, email i student_id.'}), headers={'Content-Type': 'application/json'})

        # checking if all columns have appropriate values
        for student in students_list:
            if student['first_name'] is None or student['last_name'] is None or student['email'] is None or student['student_id'] is None:
                print("Bad request. Nie wszystkie kolumny zawierają wartości.")
                return HttpResponseBadRequest(json.dumps({'name': 'Nie wszystkie kolumny zawierają wartości.'}), headers={'Content-Type': 'application/json'})
            if not email_validation(student['email']):
                print("Bad request. Niepoprawny email.")
                return HttpResponseBadRequest(json.dumps({'name': INVALID_EMAIL}), headers={'Content-Type': 'application/json'})
        

        try:
            print(group_id)
            group_to_add = Group.objects.get(id=group_id)
            print(f'Group to add: {group_to_add.name}')
        except Exception as error:
            print(error)
            return HttpResponseBadRequest(json.dumps({'name': 'Nie znaleziono grupy.'}), headers={'Content-Type': 'application/json'})


        try:
            password_generator = PasswordGenerator(10)
            if group_to_add is None:
                print('Group not found.')
                return HttpResponseBadRequest(json.dumps({'name': 'Grupa nie została znaleziona.'}), headers={'Content-Type': 'application/json'})
            
            available_edition_servers = EditionServer.objects.filter(edition__teacheredition__groups=group_to_add.id)
            if len(available_edition_servers) == 0:
                print("No available edition servers.")
                return HttpResponseBadRequest(json.dumps({'name': 'Brak serwera w danej edycji'}), headers={'Content-Type': 'application/json'})

            students_passwords = []

            for student in students_list:
                student_password = password_generator.generate_password()
                students_passwords.append(student_password)

                students_info.append({
                    'first_name': student['first_name'],
                    'last_name': student['last_name'],
                    'email': student['email'], 
                    'password': student_password,
                    'student_id': student['student_id'],
                    'student_created': '',
                    'added_to_group': '',
                    'account_created': {f"{editionServer.server.name} ({editionServer.server.provider})": {} for editionServer in available_edition_servers}
                })

            for j, student in enumerate(students_list):

                student_info_index = next((i for i, student_info in enumerate(students_info) if student_info['student_id'] == student['student_id']), None)

                if Student.objects.filter(student_id=student['student_id']).exists():
                    added_student = Student.objects.get(student_id=student['student_id'])
                    added_user = added_student.user
                    students_info[student_info_index]['student_created'] = False
                    print(f"Student {added_student.user.first_name} {added_student.user.last_name} - {added_student.student_id} already exists.")
                else:
                    added_user = User.objects.create_user(
                        first_name=student['first_name'],
                        last_name=student['last_name'],
                        email=student['email'],
                        password=students_passwords[j],
                        is_active=True,
                        is_student=True
                    )

                    added_student = Student.objects.create(
                        user=added_user,
                        student_id=student['student_id']
                    )

                    students_info[student_info_index]['student_created'] = True
                    print(f"Student {added_user.first_name} {added_user.last_name} created.")

                if added_student in group_to_add.students.all():
                    print(f"Student {added_user.first_name} {added_user.last_name} already exists in group {group_to_add.name}.")
                    students_info[student_info_index]['added_to_group'] = False
                else:
                    group_to_add.students.add(added_student)
                    print(f"Student {added_user.first_name} {added_user.last_name} added to group {group_to_add.name}.")
                    students_info[student_info_index]['added_to_group'] = True

                for edition_server in available_edition_servers:
                    username_to_add = edition_server.server.username_template.lower().replace(
                        r'{imie}', added_user.first_name.lower()).replace(
                        r'{imię}', added_user.first_name.lower()).replace(
                        r'{nazwisko}', added_user.last_name.lower()).replace(
                        r'{nr_indeksu}', added_student.student_id.lower()).replace(
                        r'{numer_indeksu}', added_student.student_id.lower()).replace(
                        r'{nr_ind}', added_student.student_id.lower()).replace(
                        r'{indeks}', added_student.student_id.lower()).replace(
                        r'{email}', added_user.email.lower()
                    )

                    if DBAccount.objects.filter(username=username_to_add, editionServer=edition_server).exists():
                        added_account = DBAccount.objects.get(username=username_to_add, editionServer=edition_server)
                        students_info[student_info_index]['account_created'][f"{edition_server.server.name} ({edition_server.server.provider})"] = False
                        print(f"Account {added_account.username} on {added_account.editionServer.server.name} ({added_account.editionServer.server.provider}) server already exists.")
                    else:
                        added_account = DBAccount.objects.create(
                            username=username_to_add, password=password_generator.generate_password(), student=added_student, editionServer=edition_server
                        )
                        students_info[student_info_index]['account_created'][f"{edition_server.server.name} ({edition_server.server.provider})"] = True
                        print(f"Added {added_account.username} on {added_account.editionServer.server.name} ({added_account.editionServer.server.provider}) server.")
            
            group_to_add.save()

        except Exception as error:
            print(f"Error: {error}")
            return HttpResponseServerError(json.dumps({"name": str(error), "students_info": students_info}), headers={'Content-Type': 'application/json'})
            
        return JsonResponse({
            "students_info": students_info
            }, status=200)


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
            return HttpResponseServerError(json.dumps({'name': str(error)}), headers={'Content-Type': 'application/json'})


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

        passwordGenerator = PasswordGenerator(8)

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
                        print(f"Account {added_account.username} on {added_account.editionServer.server.name} ({added_account.editionServer.server.provider}) server already exists.")
                        print("After if, before else")
                    else:
                        print("After else, before create")
                        if not DBAccount.objects.filter(username=username_to_add, editionServer=edition_server).exists():
                            added_account = DBAccount.objects.create(
                                username=username_to_add, password=passwordGenerator.generate_password(), student=student_to_add, editionServer=edition_server, is_moved=False
                            )
                            print("After create")
                            added_accounts.append(added_account.username)
                            print(f"Added {added_account.username} on {added_account.editionServer.server.name} ({added_account.editionServer.server.provider}) server.")                
            
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
            return HttpResponseServerError(json.dumps({'name': str(error)}), headers={'Content-Type': 'application/json'})


class RemoveStudentFromGroup(ViewSet):

    @action (methods=['post'], detail=False)
    def remove_student_from_group(self, request, format=None):\
        
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
            return HttpResponseServerError(json.dumps({'name': str(error)}), headers={'Content-Type': 'application/json'})

class ResetOwnPassword(ViewSet):

    @action (methods=['post'], detail=False)
    def reset_own_password(self, request, format=None):

        user = request.user

        if not user.has_perm('database.reset_own_password'):
            raise PermissionDenied

        passwordGenerator = PasswordGenerator()
        email_sender = EmailSender()

        try:
            account_to_reset = User.objects.get(id=user.id)
            new_password = passwordGenerator.generate_password()
            account_to_reset.set_password(new_password)
            account_to_reset.save()
            email_sender.send_email_gmail('putdb2023@gmail.com', new_password)
            print(f"Password for {account_to_reset.email} reset.")
            logout(request)
            return JsonResponse({'name': "Succesfull password reset for account of id: " + str(account_to_reset.id)}, status=200)
        except Exception as error:
            print(error)
            return HttpResponseServerError(json.dumps({'name': str(error)}), headers={'Content-Type': 'application/json'})
                

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

            passwordGenerator = PasswordGenerator()
            email_sender = EmailSender()
    
            try:
                account_to_reset = User.objects.get(id=account_id)
                new_password = passwordGenerator.generate_password()
                account_to_reset.set_password(new_password)
                account_to_reset.save()
                print("Password reseted for account: ", account_to_reset.first_name + " " + account_to_reset.last_name)
                email_sender.send_email_gmail("putdb2023@gmail.com", new_password)
                return JsonResponse({'name': "Succesfull password reset for account of id: " + str(account_to_reset.id)}, status=200)

            except Exception as error:
                print(error)
                return HttpResponseServerError(json.dumps({'name': str(error)}), headers={'Content-Type': 'application/json'})

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
                print("Password updated for account: ", account_to_update.first_name + " " + account_to_update.last_name)
                logout(request)
                return JsonResponse({'name': "Succesfull password update for account of id: " + str(account_to_update.id)}, status=200)
            else:
                print("Wrong password for account: ", account_to_update.first_name + " " + account_to_update.last_name)
                return HttpResponseBadRequest(json.dumps({'name': 'Niepoprawne hasło.'}), headers={'Content-Type': 'application/json'})
        except Exception as error:
            print(error)
            return HttpResponseServerError(json.dumps({'name': str(error)}), headers={'Content-Type': 'application/json'})


        