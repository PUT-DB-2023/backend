from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
import MySQLdb as mdb

from .serializers import UserSerializer, AdminSerializer, TeacherSerializer, StudentSerializer, RoleSerializer, UserRoleSerializer, PermissionSerializer, RolePermissionSerializer, CourseSerializer, SemesterSerializer, EditionSerializer, TeacherEditionSerializer, GroupSerializer, ServerSerializer, EditionServerSerializer, StudentGroupSerializer, DBAccountSerializer
from .models import User, Admin, Teacher, Student, Role, UserRole, Permission, RolePermission, Course, Semester, Edition, TeacherEdition, Group, Server, EditionServer, StudentGroup, DBAccount


class UserViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting users.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'password', 'email', 'first_name', 'last_name']

class AdminViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting admins.
    """
    serializer_class = AdminSerializer
    queryset = Admin.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'password', 'email', 'first_name', 'last_name']

class TeacherViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting teachers.
    """
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'password', 'email', 'first_name', 'last_name']

class StudentViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting students.
    """
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'password', 'email', 'first_name', 'last_name', 'student_id']

class RoleViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting roles.
    """
    serializer_class = RoleSerializer
    queryset = Role.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'name', 'description']

class UserRoleViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting user roles.
    """
    serializer_class = UserRoleSerializer
    queryset = UserRole.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'id',
        'user',
        'role',
        'user__first_name',
        'user__last_name',
        'user__email',
        'user__password',
        'role__name',
        'role__description',
    ]

class PermissionViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting permissions.
    """
    serializer_class = PermissionSerializer
    queryset = Permission.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'name', 'description']

class RolePermissionViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting role permissions.
    """
    serializer_class = RolePermissionSerializer
    queryset = RolePermission.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'id', 
        'role', 
        'permission',
        'role',
        'permission',
        'role__name',
        'permission__name',
    ]

class CourseViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting courses.
    """
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'name', 'description']

class SemesterViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting semesters.
    """
    serializer_class = SemesterSerializer
    queryset = Semester.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'year', 'winter']

class EditionViewSet(viewsets.ModelViewSet):
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
        'active', 
        'course', 
        'semester', 
        'semester__year', 
        'semester__winter', 
        'course__name',
        'course__description',
    ]

class TeacherEditionViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting teachers in editions.
    """
    serializer_class = TeacherEditionSerializer
    queryset = TeacherEdition.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'id',
        'teacher',
        'edition',
        'edition__description',
        'edition__date_opened',
        'edition__date_closed',
        'edition__active',
        'edition__course',
        'edition__semester',
        'edition__semester__year',
        'edition__semester__winter',
        'edition__course__name',
        'teacher__id',
        'teacher__password',
        'teacher__email',
        'teacher__first_name',
        'teacher__last_name',
    ]

class GroupViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting groups.
    """
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'id', 
        'name', 
        'day', 
        'hour', 
        'room', 
        'teacherEdition', 
        'teacherEdition__edition', 
        'teacherEdition__edition__course', 
        'teacherEdition__edition__semester', 
        'teacherEdition__edition__semester__year', 
        'teacherEdition__edition__semester__winter', 
        'teacherEdition__edition__course__name', 
        'teacherEdition__teacher', 
        'teacherEdition__teacher__first_name', 
        'teacherEdition__teacher__last_name'
    ]

class ServerViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting servers.
    """
    serializer_class = ServerSerializer
    queryset = Server.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'name', 'ip', 'port', 'date_created', 'active']

class EditionServerViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting edition servers.
    """
    serializer_class = EditionServerSerializer
    queryset = EditionServer.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'id', 
        'edition', 
        'server', 
        'additional_info', 
        'edition__description', 
        'edition__date_opened', 
        'edition__date_closed', 
        'edition__active', 
        'edition__course', 
        'edition__semester', 
        'edition__semester__year', 
        'edition__semester__winter', 
        'edition__course__name', 
        'server__name', 
        'server__ip', 
        'server__port', 
        'server__date_created', 
        'server__active'
    ]

class StudentGroupViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting student groups.
    """
    serializer_class = StudentGroupSerializer
    queryset = StudentGroup.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'id', 
        'student', 
        'group',
        'student__first_name',
        'student__last_name',
        'group__name',
        'group__day',
        'group__hour',
        'group__room',
        'group__teacherEdition',
        'group__teacherEdition__edition',
        'group__teacherEdition__edition__course',
        'group__teacherEdition__edition__semester',
        'group__teacherEdition__edition__semester__year',
        'group__teacherEdition__edition__semester__winter',
        'group__teacherEdition__edition__course__name',
        'group__teacherEdition__teacher',
        'group__teacherEdition__teacher__first_name',
        'group__teacherEdition__teacher__last_name'
    ]

class DBAccountViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting db accounts.
    """
    serializer_class = DBAccountSerializer
    queryset = DBAccount.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'id', 
        'username', 
        'password', 
        'editionServer', 
        'additional_info', 
        'student',
        'editionServer__edition',
        'editionServer__server',
        'editionServer__additional_info',
        'editionServer__edition__description',
        'editionServer__edition__date_opened',
        'editionServer__edition__date_closed',
        'editionServer__edition__active',
        'editionServer__edition__course',
        'editionServer__edition__semester',
        'editionServer__edition__semester__year',
        'editionServer__edition__semester__winter',
        'editionServer__edition__course__name',
        'editionServer__server__name',
        'editionServer__server__ip',
        'editionServer__server__port',
        'editionServer__server__date_created',
        'editionServer__server__active',
        'student__first_name',
        'student__last_name',
        'student__student_id',
    ]

class AddUserAccountToExternalDB(viewsets.ViewSet):
    @action (methods=['post'], detail=False)

    def add_db_account(self, request, format=None):
        user_data = request.data
        conn = mdb.connect(host='localhost', port=3306, user='root', passwd='root', db='lab')
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO students (first_name, last_name, email, password, student_id) VALUES (%s, %s, %s, %s, %s)", (user_data['first_name'], user_data['last_name'], user_data['email'], user_data['password'], user_data['student_id']))
            conn.commit()
            return Response({'status': 'ok'})
        except:
            conn.rollback()
            print("Error")
        finally:
            conn.close()
            print("Successfully added a new user to an external DB")
        return Response({'status': 'bad'})