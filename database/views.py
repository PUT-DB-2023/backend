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
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse, HttpResponseServerError, HttpResponseNotFound
from django.db import IntegrityError
import json


import MySQLdb as mdb
from database.password_generator import PasswordGenerator
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
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError as error:
            if "unique_semester" in str(error):
                return HttpResponseBadRequest(json.dumps({'name': 'Semestr już istnieje.'}), headers={'Content-Type': 'application/json'})
            return HttpResponseBadRequest(json.dumps({'name': str(error)}), headers={'Content-Type': 'application/json'})

    def update(self, request, *args, **kwargs):
        if request.data.get('active') == True:
            Semester.objects.all().update(active=False)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        semester = self.get_object()
        if semester.active:
            return HttpResponseBadRequest(json.dumps({'name': 'Nie można usunąć aktywnego semestru.'}), headers={'Content-Type': 'application/json'})
        if semester.editions.count() > 0:
            return HttpResponseBadRequest(json.dumps({'name': 'Nie można usunąć semestru, który ma przypisane edycje.'}), headers={'Content-Type': 'application/json'})
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

    def create(self, request, *args, **kwargs):
        print(request.data)
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
            return HttpResponseBadRequest(json.dumps({'name': str(error)}), headers={'Content-Type': 'application/json'})
        # except Exception as error:
        #     return HttpResponseBadRequest("Unknown error: ", error)

    def update(self, request, *args, **kwargs):
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
            # current_servers = [server.id for server in edition.servers.all()]

            # for current_teacher in current_teachers:
            #     if current_teacher not in teachers:
            #         if TeacherEdition.objects.filter(teacher=current_teacher, edition=edition).exists():
            #             TeacherEdition.objects.filter(teacher=current_teacher, edition=edition).delete()
            #         TeacherEdition.objects.filter(teacher=current_teacher, edition=edition).delete()

            # check if missing teachers do not have any groups in this edition
            for current_teacher in current_teachers:
                if current_teacher not in teachers:
                    teacher_edition = TeacherEdition.objects.get(teacher=current_teacher, edition=edition)
                    print(f"Teacher edition: {teacher_edition}")
                    if Group.objects.filter(teacherEdition=teacher_edition).exists():
                        return HttpResponseBadRequest(json.dumps({'name': 'Nie można usunąć nauczyciela, który ma przypisane grupy.'}), headers={'Content-Type': 'application/json'})
            
            # check if missing servers do not have any groups in this edition
            # for current_server in current_servers:
            #     if current_server not in servers:
            #         if Group.objects.filter(server=current_server, edition=edition).exists():
            #             return HttpResponseBadRequest(json.dumps({'name': 'Nie można usunąć serwera, z którego korzystają grupy.'}), headers={'Content-Type': 'application/json'})


            edition.teachers.set(teachers)
            edition.servers.set(servers)

            edition.save()
            print(f"Edition updated: {edition}")

            # TeacherEdition.objects.filter(edition=edition).delete()
            # TeacherEdition.objects.bulk_create([
            #     TeacherEdition(teacher=Teacher.objects.get(id=teacher), edition=edition)
            #     for teacher in teachers
            # ])
            # for teacher in teachers:
            #     teacher_edition = TeacherEdition.objects.get_or_create(edition=edition, teacher=teacher)
            #     teacher_edition.teacher = Teacher.objects.get(id=teacher)
            #     teacher_edition.save()
            # print(f"Teachers added: {teachers}")

            # for server in servers:
            #     edition_server = EditionServer.objects.get_or_create(edition=edition, server=server)
            #     edition_server.server = Server.objects.get(id=server)
            #     edition_server.save()
            # # EditionServer.objects.filter(edition=edition).delete()
            # # EditionServer.objects.bulk_create([
            # #     EditionServer(server=Server.objects.get(id=server), edition=edition)
            # #     for server in servers
            # # ])
            # print(f"Servers added: {servers}")
            return Response(EditionSerializer(edition).data, status=200)
            # super().update(request, *args, **kwargs)
        except IntegrityError as error:
            if "unique_edition" in str(error):
                return HttpResponseBadRequest(json.dumps({'name': 'Edycja już istnieje.'}), headers={'Content-Type': 'application/json'})
            return HttpResponseBadRequest(json.dumps({'name': str(error)}), headers={'Content-Type': 'application/json'})
        # except Exception as error:
        #     return HttpResponseBadRequest("Unknown error: ", error)
    
    def destroy(self, request, *args, **kwargs):
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
        except IntegrityError as error:
            return HttpResponseBadRequest(json.dumps({'name': str(error)}), headers={'Content-Type': 'application/json'})
        # except Exception as error:
        #     return HttpResponseBadRequest("Unknown error: ", error)


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

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        all_accounts_moved = True
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
            server = Server.objects.get(id=accounts_data['server_id'])
            return HttpResponseBadRequest(json.dumps({'name': f"Wszystkie konta w grupie zostały już utworzone w zewnętrznej bazie danych ({server.name} - {server.provider})."}), headers={'Content-Type': 'application/json'})

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
                    cursor.execute('DROP ROLE IF EXISTS "%s";' % (account.username)) # TODO: implement checking if user exists
                    cursor.execute(server.create_user_template % (account.username, account.password))
                    moved_accounts.append(account.username)
                    DBAccount.objects.filter(id=account.id).update(is_moved=True)
                    print(f"Successfully created user '{account.username}' with '{account.password}' password.")
                conn_postgres.commit()
                cursor.close()
                conn_postgres.close()
                return JsonResponse({'moved_accounts': moved_accounts}, status=200)

            except (Exception) as error:
                print(error)
                # if error.
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
                return Response(json.dumps({
                    'moved_accounts': moved_accounts
                }), headers={'Content-Type': 'application/json'}, status=200)
            except (Exception) as error:
                print(error)
                return HttpResponseServerError(json.dumps({'name': str(error)}), headers={'Content-Type': 'application/json'})
        else:
            return HttpResponseBadRequest(json.dumps({'name': 'Unknown provider.'}), headers={'Content-Type': 'application/json'})


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

        
        return HttpResponseBadRequest(json.dumps({'name': 'Unknown provider.'}), headers={'Content-Type': 'application/json'})


class LoadStudentsFromCSV(ViewSet):

    @action (methods=['post'], detail=False)
    def load_students_csv(self, request, format=None):
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
        except Exception as error:
            print('Błędny plik csv.', error)
            return HttpResponseNotFound(json.dumps({'name': 'Błąd podczas wczytywania pliku csv. Upewnij się czy próbujesz przesłać poprawny plik (z kodowaniem UTF-8).'}), headers={'Content-Type': 'application/json'})

        students_info = []

        if 'first_name' not in students_list[0] or 'last_name' not in students_list[0] or 'email' not in students_list[0] or 'student_id' not in students_list[0]:
            print("Bad request. Błędny plik csv.")
            return HttpResponseBadRequest(json.dumps({'name': 'Błędny plik csv. Upewnij się, że zawiera on następujące kolumny: first_name, last_name, email i student_id.'}), headers={'Content-Type': 'application/json'})

        try:
            print(group_id)
            group_to_add = Group.objects.get(id=group_id)
            print(f'Group to add: {group_to_add.name}')
        except Exception as error:
            print(error)
            return HttpResponseBadRequest(json.dumps({'name': 'Nie znaleziono grupy.'}), headers={'Content-Type': 'application/json'})


        try:
            passwordGenerator = PasswordGenerator(8)
            if group_to_add is None:
                print('Group not found.')
                return HttpResponseBadRequest(json.dumps({'name': 'Grupa nie została znaleziona.'}), headers={'Content-Type': 'application/json'})
            
            available_edition_servers = EditionServer.objects.filter(edition__teacheredition__group=group_to_add.id)
            if len(available_edition_servers) == 0:
                print("No available edition servers.")
                return HttpResponseBadRequest(json.dumps({'name': 'Brak serwera w danej edycji'}), headers={'Content-Type': 'application/json'})

            students_passwords = []

            for student in students_list:
                student_password = passwordGenerator.generate_password()
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
                    students_info[student_info_index]['student_created'] = False
                    print(f"Student {added_student.first_name} {added_student.last_name} - {added_student.student_id} already exists.")
                else:
                    added_student = Student.objects.create(
                        first_name=student['first_name'],
                        last_name=student['last_name'],
                        email=student['email'],
                        password=students_passwords[j],
                        student_id=student['student_id'])

                    students_info[student_info_index]['student_created'] = True
                    print(f"Student {added_student.first_name} {added_student.last_name} created.")

                if added_student in group_to_add.students.all():
                    print(f"Student {added_student.first_name} {added_student.last_name} already exists in group {group_to_add.name}.")
                    students_info[student_info_index]['added_to_group'] = False # TODO: check if this works
                else:
                    group_to_add.students.add(added_student)
                    print(f"Student {added_student.first_name} {added_student.last_name} added to group {group_to_add.name}.")
                    students_info[student_info_index]['added_to_group'] = True

                for edition_server in available_edition_servers:
                    username_to_add = edition_server.server.username_template.lower().replace(
                        r'{imie}', added_student.first_name.lower()).replace(
                        r'{imię}', added_student.first_name.lower()).replace(
                        r'{nazwisko}', added_student.last_name.lower()).replace(
                        r'{nr_indeksu}', added_student.student_id.lower()).replace(
                        r'{numer_indeksu}', added_student.student_id.lower()).replace(
                        r'{nr_ind}', added_student.student_id.lower()).replace(
                        r'{indeks}', added_student.student_id.lower()).replace(
                        r'{email}', added_student.email.lower()
                    )

                    if DBAccount.objects.filter(username=username_to_add, editionServer=edition_server).exists():
                        added_account = DBAccount.objects.get(username=username_to_add, editionServer=edition_server)
                        students_info[student_info_index]['account_created'][f"{edition_server.server.name} ({edition_server.server.provider})"] = False
                        print(f"Account {added_account.username} on {added_account.editionServer.server.name} ({added_account.editionServer.server.provider}) server already exists.")
                    else:
                        added_account = DBAccount.objects.create(
                            username=username_to_add, password=passwordGenerator.generate_password(), student=added_student, editionServer=edition_server
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

        available_edition_servers = EditionServer.objects.filter(edition__teacheredition__group=group_to_add.id)
        print(available_edition_servers)
        
        if len(available_edition_servers) == 0:
            print("No available edition servers.")
            return HttpResponseBadRequest(json.dumps({'name': 'Brak serwera w danej edycji'}), headers={'Content-Type': 'application/json'})

        passwordGenerator = PasswordGenerator(8)

        try:
            for student_id in students:
                student_to_add = Student.objects.get(id=student_id)
                if student_to_add in group_to_add.students.all():
                    print(f"Student {student_to_add.first_name} {student_to_add.last_name} already exists in group {group_to_add.name}.")
                else:
                    group_to_add.students.add(student_to_add)
                    print(f"Student {student_to_add.first_name} {student_to_add.last_name} added to group {group_to_add.name}.")
                    added_students.append(F"{student_to_add.first_name} {student_to_add.last_name} - {student_to_add.student_id}")

                for edition_server in available_edition_servers:
                    username_to_add = edition_server.server.username_template.lower().replace(
                        r'{imie}', student_to_add.first_name.lower()).replace(
                        r'{imię}', student_to_add.first_name.lower()).replace(
                        r'{nazwisko}', student_to_add.last_name.lower()).replace(
                        r'{nr_indeksu}', student_to_add.student_id.lower()).replace(
                        r'{numer_indeksu}', student_to_add.student_id.lower()).replace(
                        r'{nr_ind}', student_to_add.student_id.lower()).replace(
                        r'{indeks}', student_to_add.student_id.lower()).replace(
                        r'{email}', student_to_add.email.lower()
                    )

                    if DBAccount.objects.filter(username=username_to_add, editionServer=edition_server).exists():
                        added_account = DBAccount.objects.get(username=username_to_add, editionServer=edition_server)
                        print(f"Account {added_account.username} on {added_account.editionServer.server.name} ({added_account.editionServer.server.provider}) server already exists.")
                    else:
                        added_account = DBAccount.objects.create(
                            username=username_to_add, password=passwordGenerator.generate_password(), student=student_to_add, editionServer=edition_server, is_moved=False
                        )
                        added_accounts.append(added_account.username)
                        print(f"Added {added_account.username} on {added_account.editionServer.server.name} ({added_account.editionServer.server.provider}) server.")
            
            group_to_add.save()
            print('Added students: ', added_students)

            return JsonResponse({
                'added_students': added_students,
                'added_accounts': added_accounts
                }, status=200)

        except Exception as error:
            print(error)
            return HttpResponseServerError(json.dumps({'name': str(error)}), headers={'Content-Type': 'application/json'})


class RemoveStudentFromGroup(ViewSet):

    @action (methods=['post'], detail=False)
    def remove_student_from_group(self, request, format=None):
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