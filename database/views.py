from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
# from rest_framework_serializer_extensions.views import SerializerExtensionsAPIViewMixin
from django_filters.rest_framework import DjangoFilterBackend
import MySQLdb as mdb
import psycopg2

from .serializers import UserSerializer, AdminSerializer, TeacherSerializer, StudentSerializer, RoleSerializer, PermissionSerializer, CourseSerializer, SemesterSerializer, EditionSerializer, TeacherEditionSerializer, GroupSerializer, ServerSerializer, EditionServerSerializer, DBAccountSerializer
from .models import User, Admin, Teacher, Student, Role, Permission, Course, Semester, Edition, TeacherEdition, Group, Server, EditionServer, DBAccount


class UserViewSet(ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting users.
    """
    serializer_class = UserSerializer
    queryset = User.objects.prefetch_related('roles').all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'password', 'email', 'first_name', 'last_name']

class AdminViewSet(ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting admins.
    """
    serializer_class = AdminSerializer
    queryset = Admin.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'password', 'email', 'first_name', 'last_name']

class TeacherViewSet(ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting teachers.
    """
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'password', 'email', 'first_name', 'last_name']

class StudentViewSet(ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting students.
    """
    serializer_class = StudentSerializer
    queryset = Student.objects.prefetch_related('groups').all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'password', 'email', 'first_name', 'last_name', 'student_id']

class RoleViewSet(ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting roles.
    """
    serializer_class = RoleSerializer
    queryset = Role.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'name', 'description']

class PermissionViewSet(ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting permissions.
    """
    serializer_class = PermissionSerializer
    queryset = Permission.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'name', 'description']

class CourseViewSet(ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting courses.
    """
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'name', 'description']

class SemesterViewSet(ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting semesters.
    """
    serializer_class = SemesterSerializer
    queryset = Semester.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'year', 'winter']

class EditionViewSet(ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting editions.
    """
    serializer_class = EditionSerializer
    queryset = Edition.objects.prefetch_related('teachers').select_related('course', 'semester')
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
        'teachers',
        'teachers__first_name',
        'teachers__last_name',
    ]

class TeacherEditionViewSet(ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting teachers in editions.
    """
    serializer_class = TeacherEditionSerializer
    queryset = TeacherEdition.objects.select_related('teacher', 'edition')
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

class GroupViewSet(ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting groups.
    """
    serializer_class = GroupSerializer
    queryset = Group.objects.prefetch_related('students').select_related('teacherEdition')
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


class ServerViewSet(ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting servers.
    """
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
        'edition__course__description',
    ]

class EditionServerViewSet(ModelViewSet):
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

class DBAccountViewSet(ModelViewSet):
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
        'isMovedToExtDB',
    ]

class AddUserAccountToExternalDB(ViewSet):
    @action (methods=['post'], detail=False)
    def add_db_account(self, request, format=None):
        print('Request log:', request.data)
        user_data = request.data

        conn_postgres = psycopg2.connect(
            host="postgres",
            database="postgres",
            user="postgres",
            password="postgres",
            port=5432)
        
        try:
            cur = conn_postgres.cursor()
            cur.execute('select dd.username, dd.password, dd.id from database_server dser inner join (database_editionserver de inner join (database_dbaccount dd inner join (database_group_students ds inner join database_group dg on ds.group_id = dg.id) on dd.student_id = ds.student_id) on de.id = dd."editionServer_id") on dser.id = de.server_id where dser.id=%s and dg.id=%s and dd."isMovedToExtDB" = false;', (user_data['serverID'], user_data['groupID']))
            userIDS = cur.fetchall()
            print("Select result: ", userIDS)
            DB_IDS = [el[2] for el in userIDS]
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn_postgres is not None:
                conn_postgres.close()
                print('Database connection closed.')
            

        conn_mysql = mdb.connect(host='localhost', port=3306, user='root', passwd='root', db='mysql')
        try:
            cursor = conn_mysql.cursor()
            print(userIDS)
            if len(userIDS) == 0:
                return Response({'status': 'empty'})
            for user in userIDS:
                cursor.execute("CREATE USER IF NOT EXISTS %s@'localhost' IDENTIFIED BY %s;", (user[0], user[1]))
                
            conn_mysql.commit()
            print(DB_IDS)
            DBAccount.objects.filter(id__in=DB_IDS).update(isMovedToExtDB=True)
            return Response({'status': 'ok'})
        except (Exception, mdb.DatabaseError) as error:
            print(error)
            conn_mysql.rollback()
        finally:
            conn_mysql.close()
        return Response({'status': 'bad'})