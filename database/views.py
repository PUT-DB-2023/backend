import psycopg2
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
import cx_Oracle
import oracledb
from pymongo import MongoClient


import MySQLdb as mdb

from .serializers import UserSerializer, AdminSerializer, TeacherSerializer, StudentSerializer, RoleSerializer, PermissionSerializer, MajorSerializer, CourseSerializer, SemesterSerializer, EditionSerializer, TeacherEditionSerializer, GroupSerializer, ServerSerializer, EditionServerSerializer, DBAccountSerializer
from .models import User, Admin, Teacher, Student, Role, Permission, Major, Course, Semester, Edition, TeacherEdition, Group, Server, EditionServer, DBAccount


class UserViewSet(ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting users.
    """
    serializer_class = UserSerializer
    queryset = User.objects.prefetch_related('roles')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'password', 'email', 'first_name', 'last_name', 'roles',]


class AdminViewSet(ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting admins.
    """
    serializer_class = AdminSerializer
    queryset = Admin.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'password', 'email', 'first_name', 'last_name', 'roles',]


class TeacherViewSet(ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting teachers.
    """
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.prefetch_related('editions__semester', 'editions__course')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'id', 'password', 'email', 'first_name', 'last_name', 'roles',
        'editions__semester',
        'editions__semester__year',
        'editions__semester__winter',
        'editions__semester__active',
        'editions__course',
        'editions__course__name',
    ]


class StudentViewSet(ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting students.
    """
    serializer_class = StudentSerializer
    queryset = Student.objects.prefetch_related('groups', 'db_accounts')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'id', 'password', 'email', 'first_name', 'last_name', 'student_id',
        'groups', 'groups__name', 'db_accounts__editionServer__server', 'db_accounts__editionServer__server__name',
    ]


class RoleViewSet(ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting roles.
    """
    serializer_class = RoleSerializer
    queryset = Role.objects.prefetch_related('permissions', 'users')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'id', 'name', 'description',
        'permissions', 'permissions__name', 
        'users', 'users__first_name', 'users__last_name',
    ]


class PermissionViewSet(ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting permissions.
    """
    serializer_class = PermissionSerializer
    queryset = Permission.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'id', 'name', 'description',
        'roles', 'roles__name', 'roles__users', 'roles__users__first_name', 'roles__users__last_name',
    ]


class MajorViewSet(ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting majors.
    """
    serializer_class = MajorSerializer
    queryset = Major.objects.prefetch_related('courses')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'name', 'courses', 'courses__name']


class CourseViewSet(ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting courses.
    """
    serializer_class = CourseSerializer
    queryset = Course.objects.prefetch_related('editions').order_by('id')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'name', 'major', 'active', 'description', 'editions']

    # def get_queryset(self):
    #     if self.request.query_params.get('active') == "true":
    #         return Course.objects.prefetch_related('editions').filter(editions__semester__active=True).distinct().order_by('id')
    #     elif self.request.query_params.get('active') == "false":
    #         return Course.objects.prefetch_related('editions').exclude(editions__semester__active=True).distinct().order_by('id')
    #     else:
    #         return Course.objects.prefetch_related('editions').order_by('id')


class SemesterViewSet(ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting semesters.
    """
    serializer_class = SemesterSerializer
    queryset = Semester.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'year', 'winter', 'active', 'editions']


class EditionViewSet(ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting editions.
    """
    serializer_class = EditionSerializer
    queryset = Edition.objects.prefetch_related('teachers', 'servers').select_related('course', 'semester')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'id', 
        'description', 
        'date_opened', 
        'date_closed',
        'semester', 
        'semester__year', 
        'semester__winter', 
        'semester__active',
        'course', 
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
    queryset = TeacherEdition.objects.select_related('teacher', 'edition__semester', 'edition__course').prefetch_related('edition__servers').order_by('id')
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
        'edition__semester__year',
        'edition__semester__winter',
        'edition__semester__active',
        'edition__course__name',
        'teacher',
        'teacher__first_name',
        'teacher__last_name',
    ]


class GroupViewSet(ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting groups.
    """
    serializer_class = GroupSerializer
    queryset = Group.objects.select_related('teacherEdition__teacher', 'teacherEdition__edition__semester', 'teacherEdition__edition__course').prefetch_related('students', 'teacherEdition__edition__servers').order_by('id')
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
        'teacherEdition__edition__semester__year', 
        'teacherEdition__edition__semester__winter',
        'teacherEdition__edition__semester__active',
        'teacherEdition__edition__course', 
        'teacherEdition__edition__course__name', 
        'teacherEdition__teacher', 
        'teacherEdition__teacher__first_name', 
        'teacherEdition__teacher__last_name',
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
        'edition__semester', 
        'edition__semester__year', 
        'edition__semester__winter', 
        'edition__semester__active',
        'edition__course',
        'edition__course__name', 
        'edition__course__description',
    ]


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
        'edition__semester__year', 
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
        'editionServer__edition__semester__year',
        'editionServer__edition__semester__winter',
        'editionServer__edition__semester__active',
        'editionServer__edition__course__name',
        'editionServer__server',
        'editionServer__server__name',
        'editionServer__server__active',
        'student',
        'student__first_name',
        'student__last_name',
        'student__student_id',
    ]


class AddUserAccountToExternalDB(ViewSet):
    @action (methods=['post'], detail=False)
    def add_db_account(self, request, format=None):
        accounts_data = request.data
        print('Request log:', accounts_data)
        db_accounts = DBAccount.objects.filter(is_moved=False, editionServer__server__active=True, editionServer__server__id=accounts_data['server_id'], student__groups__id=accounts_data['group_id'])

        if not db_accounts:
            print('No accounts to move')
            return Response({'status': 'No accounts to move.'})

        server = Server.objects.get(id=accounts_data['server_id'], active=True)
        moved_accounts = []

        print(f"Server: {server}, server user: {server.user}, server password: {server.password}, server ip: {server.ip}, server port: {server.port}")
        
        if server.provider.lower() == 'mysql':  
            try:
                conn_mysql = mdb.connect(host=server.ip, port=int(server.port), user=server.user, passwd=server.password, db=server.database)
                print('Connected to MySQL server')
                cursor = conn_mysql.cursor()
                for account in db_accounts:
                    print(server.create_user_template)
                    cursor.execute(server.create_user_template % (account.username, account.password))
                    moved_accounts.append(account.username)
                    DBAccount.objects.filter(id=account.id).update(is_moved=True)
                    print(f"Successfully created user '{account.username}' with '{account.password}' password.")
                conn_mysql.commit()
                cursor.close()
                return Response({
                    'status': 'ok',
                    'moved_accounts': moved_accounts
                })

            except (Exception, mdb.DatabaseError) as error:
                print(error)
                conn_mysql.rollback()
                cursor.close()
                return Response({
                    'status': 'error',
                    'error': error
                })
            finally:
                conn_mysql.close()

        elif server.provider.lower() == 'postgres' or server.provider.lower() == 'postgresql': 
            try:
                conn_postgres = psycopg2.connect(dbname=server.database, user=server.user, password=server.password, host=server.ip, port=server.port)
                print('Connected to Postgres server')
                cursor = conn_postgres.cursor()
                for account in db_accounts:
                    print(account.username)
                    cursor.execute('DROP ROLE IF EXISTS "%s";' % (account.username))
                    cursor.execute(server.create_user_template % (account.username, account.password))
                    moved_accounts.append(account.username)
                    DBAccount.objects.filter(id=account.id).update(is_moved=True)
                    print(f"Successfully created user '{account.username}' with '{account.password}' password.")
                conn_postgres.commit()
                cursor.close()
                return Response({
                    'status': 'ok',
                    'moved_accounts': moved_accounts
                })
            except (Exception, mdb.DatabaseError) as error:
                print(error)
                conn_postgres.rollback()
                cursor.close()
                return Response({
                    'status': 'error',
                    'error': error
                })
            finally:
                conn_postgres.close()

        elif server.provider.lower() == 'mongo' or server.provider.lower() == 'mongodb':
            try:
                conn = MongoClient(f'mongodb://{server.user}:{server.password}@{server.ip}:{server.port}/')
                db = conn[server.database]
                for account in db_accounts:
                    print(account.username)
                    db.command({
                        "createUser" : account.username,
                        "pwd" : account.password,
                        "customData" : {},
                        "roles" : []
                    })
                    moved_accounts.append(account.username)
                    DBAccount.objects.filter(id=account.id).update(is_moved=True)
                    print(f"Successfully created user '{account.username}' with '{account.password}' password.")
                
                return Response({
                    'status': 'ok',
                    'moved_accounts': moved_accounts
                })
            except (Exception, mdb.DatabaseError) as error:
                print(error)
                return Response({
                    'status': 'error',
                    'error': error
                })
        elif server.provider.lower() == 'oracle' or server.provider.lower() == 'oracledb':
            try:
                conn = cx_Oracle.connect(server.user, server.password, f'{server.ip}:{server.port}/{server.database}')
                cursor = conn.cursor()
                for account in db_accounts:
                    print(account.username)
                    cursor.execute(server.create_user_template % (account.username, account.password))
                    moved_accounts.append(account.username)
                    DBAccount.objects.filter(id=account.id).update(is_moved=True)
                    print(f"Successfully created user '{account.username}' with '{account.password}' password.")
                conn.commit()
                cursor.close()
                return Response({
                    'status': 'ok',
                    'moved_accounts': moved_accounts
                })
            except (Exception, mdb.DatabaseError) as error:
                print(error)
                conn.rollback()
                cursor.close()
                return Response({
                    'status': 'error',
                    'error': error
                })
        else:
            return Response({'status': 'Unknown provider.'})


class RemoveUserFromExternalDB(ViewSet):
    @action (methods=['post'], detail=False)
    def delete_db_account(self, request, format=None):
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
                print(f"Successfully deleted user '{db_account.username}'")
                return Response({'status': 'ok',
                    'deleted_account': db_account.username})
            except (Exception, mdb.DatabaseError) as error:
                print(error)
                conn_mysql.rollback()
                cursor.close()
                return Response({
                    'status': 'error',
                    'error': error
                })
            finally:
                conn_mysql.close()
                
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
                return Response({'status': 'ok',
                    'deleted_account': db_account.username})
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
                conn_postgres.rollback()
                cursor.close()
                return Response({
                    'status': 'error',
                    'error': error
                })
            finally:
                conn_postgres.close()

        elif db_account_server_provider.lower() == 'mongo' or db_account_server_provider.lower() == 'mongodb':
            try:
                conn = MongoClient(f'mongodb://{db_account.editionServer.server.user}:{db_account.editionServer.server.password}@{db_account.editionServer.server.ip}:{db_account.editionServer.server.port}/')
                db = conn[db_account.editionServer.server.database]
                db.command({
                    "dropUser" : db_account.username
                })
                DBAccount.objects.filter(id=db_account.id).update(is_moved=False)
                print(f"Successfully deleted user '{db_account.username}'")
                return Response({'status': 'ok',
                    'deleted_account': db_account.username})
            except (Exception, mdb.DatabaseError) as error:
                print(error)
                # client.rollback()
                return Response({
                    'status': 'error',
                    'error': error
                })

        
        return Response({'status': 'ok'})