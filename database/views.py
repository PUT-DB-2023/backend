import psycopg2
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
import cx_Oracle
import oracledb
# import pyodbc
from pymongo import MongoClient
import csv
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.db import IntegrityError


import MySQLdb as mdb

from .serializers import UserSerializer, AdminSerializer, TeacherSerializer, StudentSerializer, RoleSerializer, PermissionSerializer, MajorSerializer, CourseSerializer, SemesterSerializer, BasicSemesterSerializer, EditionSerializer, TeacherEditionSerializer, GroupSerializer, ServerSerializer, EditionServerSerializer, DBAccountSerializer, SimpleTeacherEditionSerializer
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
        'editions__semester__start_year',
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
    queryset = Semester.objects.prefetch_related('editions')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'start_year', 'winter', 'active', 'editions']

    def create(self, request, *args, **kwargs):
        # if request.data.get('active') == True:
        #     Semester.objects.all().update(active=False)
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError as e:
            if "unique_semester" in str(e):
                return HttpResponseBadRequest("Semester already exists")
            return HttpResponseBadRequest("Unknown error: ", e)
    
    # def destroy(self, request, *args, **kwargs):
    #     if self.get_object().active:
    #         print("Cannot delete active semester")
    #         return HttpResponseBadRequest("Cannot delete active semester")
    #     print("Deleting semester")
    #     return super().delete(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if request.data.get('active') == True:
            Semester.objects.all().update(active=False)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        semester = self.get_object()
        if semester.active:
            return HttpResponseBadRequest("Cannot delete active semester")
        if semester.editions.count() > 0:
            return HttpResponseBadRequest("Cannot delete semester with editions")
        return super().destroy(request, *args, **kwargs)


class SimpleSemesterViewSet(ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting semesters.
    """
    serializer_class = BasicSemesterSerializer
    queryset = Semester.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'start_year', 'winter', 'active', 'editions']


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
        'semester__start_year', 
        'semester__winter', 
        'semester__active',
        'course', 
        'course__name',
        'course__description',
        'teachers',
        'teachers__first_name',
        'teachers__last_name',
    ]

    def get_queryset(self):
        if self.request.query_params.get('basic') == "true":
            return Edition.objects.only('id', 'course_id', 'semester_id')
        else:
            return Edition.objects.prefetch_related('teachers', 'servers').select_related('course', 'semester')


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
        'edition__semester__start_year',
        'edition__semester__winter',
        'edition__semester__active',
        'edition__course__name',
        'teacher',
        'teacher__first_name',
        'teacher__last_name',
    ]


class SimpleTeacherEditionViewSet(ModelViewSet):
    """
    A simple ViewSet for listing, retrieving and posting teachers in editions.
    """
    serializer_class = SimpleTeacherEditionSerializer
    queryset = TeacherEdition.objects.select_related('teacher').only('id', 'teacher_id')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'id',
        'teacher',
        'teacher__first_name',
        'teacher__last_name',
        'edition',
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
        'edition__semester__start_year', 
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
            return HttpResponse('No accounts to move.', status=400)

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
                conn_mysql.close()

                return JsonResponse({'moved_accounts': moved_accounts}, status=200)

            except (Exception, mdb.DatabaseError) as error:
                print("error: ", error)
                return HttpResponse(error, status=500)

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
                    cursor.execute('DROP ROLE IF EXISTS "%s";' % (account.username))
                    cursor.execute(server.create_user_template % (account.username, account.password))
                    moved_accounts.append(account.username)
                    DBAccount.objects.filter(id=account.id).update(is_moved=True)
                    print(f"Successfully created user '{account.username}' with '{account.password}' password.")
                conn_postgres.commit()
                cursor.close()
                conn_postgres.close()
                return JsonResponse({'moved_accounts': moved_accounts}, status=200)

            except (Exception, mdb.DatabaseError) as error:
                print(error)
                return HttpResponse(error, status=500)

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
                        continue
                    else:
                        db.command('createUser', account.username, pwd=account.password, roles=[{'role': 'readWrite', 'db': server.database}])
                        moved_accounts.append(account.username)
                        DBAccount.objects.filter(id=account.id).update(is_moved=True)
                        print(f"Successfully created user '{account.username}' with '{account.password}' password.")
                conn.close()
                return JsonResponse({'moved_accounts': moved_accounts}, status=200)
            except (Exception, mdb.DatabaseError) as error:
                print(error)
                return HttpResponse(error, status=500)

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
                return HttpResponse(error, status=500)
        else:
            return HttpResponse('Unknown provider.', status=400)


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
                conn_mysql.close()
                print(f"Successfully deleted user '{db_account.username}'")
                return HttpResponse(f'deleted_account: {db_account.username}', status=200)
            except (Exception, mdb.DatabaseError) as error:
                print(error)
                return HttpResponse(error, status=500)
                
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
                return HttpResponse(error, status=500)


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
                print(error)
                return HttpResponse(error, status=500)

        
        return HttpResponse('Unknown provider.', status=400)


class LoadStudentsFromCSV(ViewSet):

    @action (methods=['post'], detail=False)
    def load_students_csv(self, request, format=None):
        accounts_data = request.data
        print('Request log:', accounts_data)

        if 'group_id' not in accounts_data or 'students_csv' not in accounts_data:
            print('Error: group_id or students_csv not found in request data.')
            return HttpResponseBadRequest('Group_id or students_csv not found in request data.')

            
        group_id = accounts_data['group_id']
        students_csv = accounts_data['students_csv']

        students_csv = students_csv.read().decode('utf-8-sig')
        csv_reader = csv.DictReader(students_csv.splitlines(), delimiter=',')
        students_list = list(csv_reader)

        created_students = []

        students_info = []

        if 'first_name' not in students_list[0] or 'last_name' not in students_list[0] or 'email' not in students_list[0] or 'password' not in students_list[0] or 'student_id' not in students_list[0]:
            print("Bad request. Invalid CSV file.")
            return HttpResponseBadRequest('Invalid CSV file.', status=400)

        try:
            print(group_id)
            group_to_add = Group.objects.get(id=group_id)
            print(f'Group to add: {group_to_add.name}')
            if group_to_add is None:
                print('Group not found.')
                return HttpResponseBadRequest('Group not found.', status=400)
            
            available_editionServers = EditionServer.objects.filter(edition__teacheredition__group=group_to_add.id)
            if len(available_editionServers) == 0:
                print("No available edition servers.")
                return HttpResponseBadRequest('No edition servers available for this group.', status=400)

            for student in students_list:
                added_student, created = Student.objects.get_or_create(
                    first_name=student['first_name'],
                    last_name=student['last_name'],
                    email=student['email'],
                    password=student['password'], # TODO: generate password
                    student_id=student['student_id'])
                
                students_info.append({
                    'first_name': student['first_name'],
                    'last_name': student['last_name'],
                    'email': student['email'],
                    'password': student['password'],
                    'student_id': student['student_id'],
                    'student_created': '',
                    'added_to_group': '',
                    'account_created': {},})

                if not created:
                    students_info[-1]['student_created'] = False
                    print(f"Student {added_student.first_name} {added_student.last_name} already exists.")
                else:
                    students_info[-1]['student_created'] = True
                    print(f"Student {added_student.first_name} {added_student.last_name} created.")
                created_students.append(added_student)

                if added_student in group_to_add.students.all():
                    print(f"Student {added_student.first_name} {added_student.last_name} already exists in group {group_to_add.name}.")
                    students_info[-1]['added_to_group'] = False # TODO: check if this works
                else:
                    group_to_add.students.add(added_student)
                    print(f"Student {added_student.first_name} {added_student.last_name} added to group {group_to_add.name}.")
                    students_info[-1]['added_to_group'] = True

                for editionServer in available_editionServers:
                    username_to_add = editionServer.username_template.lower().replace(
                        r'{imie}', added_student.first_name.lower()).replace(
                        r'{imię}', added_student.first_name.lower()).replace(
                        r'{nazwisko}', added_student.last_name.lower()).replace(
                        r'{nr_indeksu}', added_student.student_id.lower()).replace(
                        r'{numer_indeksu}', added_student.student_id.lower()).replace(
                        r'{nr_ind}', added_student.student_id.lower()).replace(
                        r'{indeks}', added_student.student_id.lower()).replace(
                        r'{email}', added_student.email.lower()
                        )

                    added_account, created = DBAccount.objects.get_or_create(
                        username=username_to_add, password=added_student.last_name + '-dbpassword', is_moved=False, student=added_student, editionServer=editionServer
                    )
                    if not created:
                        students_info[-1]['account_created'][editionServer.server.provider] = False
                        print(f"Account {added_account.username} on {added_account.editionServer.server.name} ({added_account.editionServer.server.provider}) server already exists.")
                    else:
                        students_info[-1]['account_created'][editionServer.server.provider] = True
                        print(f"Added {added_account.username} on {added_account.editionServer.server.name} ({added_account.editionServer.server.provider}) server.")
            
            group_to_add.save()


        except Exception as error:
            print(f"Error: {error}")
            return HttpResponseBadRequest(str(error), status=400)
            
        return JsonResponse({
            "students_info": students_info
            }, status=200)


class ChangeActiveSemester(ViewSet):

    @action (methods=['post'], detail=False)
    def change_active_semester(self, request, format=None):
        data = request.data
        print('Request log:', data)

        if 'semester_id' not in data:
            print('Error: semester_id not found in request data.')
            return HttpResponseBadRequest('Semester_id not found in request data.')

        semester_id = data['semester_id']

        try:
            semester_to_change = Semester.objects.get(id=semester_id)
            if semester_to_change.active:
                print('Semester is already active.')
                return HttpResponseBadRequest('Semester is already active.', status=400)
            Semester.objects.update(active=False)
            semester_to_change.active = True
            semester_to_change.save()
            return HttpResponse(status=200)
        except Exception as error:
            print(error)
            return HttpResponseBadRequest(error, status=400)


class AddStudentToGroup(ViewSet):

    @action (methods=['post'], detail=False)
    def add_student_to_group(self, request, format=None):
        data = request.data
        print('Request log:', data)

        if 'group_id' not in data:
            print('Error: group_id not found in request data.')
            return HttpResponseBadRequest('Group_id not found in request data.')

        if 'students' not in data:
            print('Error: students not found in request data.')
            return HttpResponseBadRequest('Students not found in request data.')

        group_id = data['group_id']
        students = data['students']

        added_students = []

        try:
            group_to_add = Group.objects.get(id=group_id)
        except Exception as error:
            print(error)
            return HttpResponseBadRequest('Group with this ID does not exist.', status=400)

        try:
            for student_id in students:
                student_to_add = Student.objects.get(id=student_id)
                if student_to_add in group_to_add.students.all():
                    print(f"Student {student_to_add.first_name} {student_to_add.last_name} already exists in group {group_to_add.name}.")
                else:
                    group_to_add.students.add(student_to_add)
                    print(f"Student {student_to_add.first_name} {student_to_add.last_name} added to group {group_to_add.name}.")
                    added_students.append(student_to_add.student_id)
                group_to_add.save()
                print('Added students: ', added_students)
            return JsonResponse({'added_students': added_students}, status=200)
        except Exception as error:
            print(error)
            return HttpResponseBadRequest(error, status=400)