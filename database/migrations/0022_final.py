import datetime
from django.db import migrations, models

def forwards_func(apps, schema_editor):
    ContentType = apps.get_model('contenttypes', 'ContentType')

    User = apps.get_model('database', 'User')
    Student = apps.get_model('database', 'Student')
    Teacher = apps.get_model('database', 'Teacher')
    DBAccount = apps.get_model('database', 'DBAccount')
    Group = apps.get_model('database', 'Group')
    TeacherEdition = apps.get_model('database', 'TeacherEdition')
    EditionServer = apps.get_model('database', 'EditionServer')
    Edition = apps.get_model('database', 'Edition')
    Admin = apps.get_model('database', 'Admin')
    Semester = apps.get_model('database', 'Semester')
    Course = apps.get_model('database', 'Course')
    Server = apps.get_model('database', 'Server')
    

    
    student_ct = ContentType.objects.get_for_model(Student)
    teacher_ct = ContentType.objects.get_for_model(Teacher)

    db_alias = schema_editor.connection.alias

    DBAccount.objects.all().delete()
    Group.objects.all().delete()
    TeacherEdition.objects.all().delete()
    EditionServer.objects.all().delete()
    Edition.objects.all().delete()
    Teacher.objects.all().delete()
    Student.objects.all().delete()
    Admin.objects.all().delete()
    User.objects.all().delete()
    Semester.objects.all().delete()
    Course.objects.all().delete()
    Server.objects.all().delete()

    server_names = ['Oracle ZBD Server', 'MySQL ZBD Server - OFFLINE', 'Postgres PBD Server', 'Mongo ZBDNS Server', 'Microsoft SQL Server PBD']
    server_ipss = ['128.127.80.0', '14.137.164.0', '146.112.218.0', '156.154.84.0', '176.119.32.0']
    server_ports = ['1234', '1122', '5836', '2850', '4179']
    server_date_createds = '2021-12-31'
    server_actives = [True, False, True, True, True]
    server_databases = ['oracledb', 'mysql', 'postgres', 'mongodbnosql', 'mssql']
    server_passwords = ['oracledbpass', 'mysqlpass', 'postgrespass', 'mongodbnosqlpass', 'mssqlpass']
    server_providers = ['Oracle', 'MySQL', 'Postgres', 'MongoDB', 'Microsoft SQL Server']
    server_users = ['oracledbuser', 'mysqluser', 'postgresuser', 'mongodbnosqluser', 'mssqluser']

    for i in range(len(server_names)):
        Server.objects.using(db_alias).create(
        name=server_names[i], ip=server_ipss[i], port=server_ports[i], date_created=server_date_createds, active=server_actives[i], database=server_databases[i], password=server_passwords[i], provider=server_providers[i], user=server_users[i]
    )

    course_names = ['Zarządzanie bazami danych', 'Podstawy baz danych', 'Zarządzanie bazami NoSQL', 'Projektowanie baz danych']
    course_descriptions = ['Opis kursu zarządzania bazami danych', 'Opis kursu podstaw baz danych', 'Opis kursu zarządzania bazami danych noSQL', 'Opis kursu projektowania baz danych']

    for i in range(len(course_names)):
        Course.objects.using(db_alias).create(
            name=course_names[i], description=course_descriptions[i]
    )

    semester_years = ['2019/2020', '2020/2021', '2021/2022', '2022/2023']
    semester_winters = [True, True, False, False]

    for i in range(len(semester_years)):
        Semester.objects.using(db_alias).create(
            year=semester_years[i], winter=semester_winters[i]
    )

    users_names = ["Ferdynand Dulski","Celestyn Tomaszewski","Sylwester Kaczkowski","Juri Rokicki","Pabian Archacki","Leo Zelek","Kwiatosław Greger","Hubert Kiedrowski","Waldemar Piotrowicz","Olaf Gursky","Hilary Franczak","Melchior Perzan","Świętosław Kopa","Marcin Gorniak","Oskar Kobylinski","Tymon Bialek","Gabriel Orlowski","Pankracy Grodzicki","Serwacy Watroba","Zygmunt Bilik","Aleksander Nabozny","Maryn Wyszynski","Remigiusz Ciolek","Cyprian Gracyalny","Dominik Bernacki","Szymon Rogalski","Ignacy Smigel","Ireneusz Dziak","Wisław Gielgud","Korneli Krynicki","Świętosław Lozowski","Bartłomiej Lach","Konstantyn Pitera","Franciszek Sochaczewski","Malachiasz Car","Eugeniusz Jaracz","Zbigniew Kula","Kamil Rajewski","Zenon Kosmalski","Chwalimir Bania","Romuald Mita","Ryszard Nowak","Sławomir Garstka","Tomasz Kocik","Gerwazy Cieply","Gwalbert Grodzicki","Denis Slusarczyk","Edward Przybylowicz","Malachiasz Cesarz","Iwon Capek","Dobrogost Wojtaszek","Świętosław Pawelski","Tobiasz Raczkowski","Gerard Chmiel","Bartosz Burak","Oktawiusz Ignasiak","Arkadiusz Michalak","Zdzisław Luka","Jerzy Kurcz","Julian Karczewski","Herbert Marcinkiewicz","Klemens Krzyzaniak","Metody Mioduszewski","Gościsław Niziolek","Sylwester Kaczkowski","Fryderyk Dusza","Dobrogost Wójcik","Albin Bialy","Jaromir Misiaszek","Tadeusz Galik","Bożidar Jablon","Witold Demby","Chrystian Krolikowski","Kryspyn Piekarz","Nikodem Czepiec","Wojsław Korczak","Hugo Tylka","Lubomił Ciesinski","Wisław Samborski","Bożimir Jagodzinski","Hilary Lesak","Adrian Bartel","Prot Ewy","Ludomił Kaniuk","Dobrogost Syslo","Adrian Dudzinski","Florentyn Rawski","Bożimir Banik","Wandelin Jaroszewski","Herbert Pekala","Gustaw Dobek","Oskar Jusko","Maksymilian Zajac","Bronisław Prus","Marcel Zaczek","Antoni Wiech","Przemysław Woźniak","Jakub Wróbel","Krystian Jakusik","Kamil Ambozy"]

    for i in range(10):
        Teacher.objects.using(db_alias).create(
            first_name=users_names[i].split()[0], last_name=users_names[i].split()[1], email=users_names[i].split()[0] + '.' + users_names[i].split()[1] + '@cs.put.poznan.pl' , password=users_names[i].split()[1] + '123', polymorphic_ctype_id=teacher_ct.id
    )

    for i in range(10, len(users_names)):
        Student.objects.using(db_alias).create(
            first_name=users_names[i].split()[0], last_name=users_names[i].split()[1], email=users_names[i].split()[0] + '.' + users_names[i].split()[1] + '@student.put.poznan.pl' , password=users_names[i].split()[1] + '123', student_id=str(100000+i), polymorphic_ctype_id=student_ct.id
    )

    edition_descriptions = [
        'Edycja 2019/2020 kursu Podstawy baz danych','Edycja 2019/2020 kursu Zarządzanie bazami danych', 'Edycja 2019/2020 kursu Zarządzanie bazami danych noSQL', 'Edycja 2019/2020 kursu Projektowanie baz danych',
        'Edycja 2020/2021 kursu Podstawy baz danych','Edycja 2020/2021 kursu Zarządzanie bazami danych', 'Edycja 2020/2021 kursu Zarządzanie bazami danych noSQL', 'Edycja 2020/2021 kursu Projektowanie baz danych',
        'Edycja 2021/2022 kursu Podstawy baz danych','Edycja 2021/2022 kursu Zarządzanie bazami danych', 'Edycja 2021/2022 kursu Zarządzanie bazami danych noSQL', 'Edycja 2021/2022 kursu Projektowanie baz danych',
        'Edycja 2022/2023 kursu Podstawy baz danych','Edycja 2022/2023 kursu Zarządzanie bazami danych', 'Edycja 2022/2023 kursu Zarządzanie bazami danych noSQL', 'Edycja 2022/2023 kursu Projektowanie baz danych'
        ]

    dates_opened = [
        '2019-10-01', '2019-10-01', '2019-10-01', '2019-10-01',
        '2020-10-01', '2020-10-01', '2020-10-01', '2020-10-01',
        '2021-10-01', '2021-10-01', '2021-10-01', '2021-10-01',
        '2022-10-01', '2022-10-01', '2022-10-01', '2022-10-01'
    ]

    dates_closed = [
        '2020-06-30', '2020-06-30', '2020-06-30', '2020-06-30',
        '2021-06-30', '2021-06-30', '2021-06-30', '2021-06-30',
        '2022-06-30', '2022-06-30', '2022-06-30', '2022-06-30',
        None, None, None, None
    ]

    actives = [
        False, False, False, False,
        False, False, False, False,
        False, False, False, False,
        True, True, True, True
    ]

    courses = Course.objects.all().values_list('id', flat=True)

    courses_ids = [
    courses[1], courses[0], courses[2], courses[3],
    courses[1], courses[0], courses[2], courses[3],
    courses[1], courses[0], courses[2], courses[3],
    courses[1], courses[0], courses[2], courses[3]]

    semesters = Semester.objects.all().values_list('id', flat=True)

    semestres_ids = [
        semesters[0], semesters[0], semesters[0], semesters[0],
        semesters[1], semesters[1], semesters[1], semesters[1],
        semesters[2], semesters[2], semesters[2], semesters[2],
        semesters[3], semesters[3], semesters[3], semesters[3]
    ]

    for i in range(len(edition_descriptions)):
        Edition.objects.using(db_alias).create(
            description=edition_descriptions[i], date_opened=dates_opened[i], date_closed=dates_closed[i], active=actives[i], course_id=courses_ids[i], semester_id=semestres_ids[i]
    )

    edition_server_add_info = [
        'Additional info about EditionServer','Additional info about EditionServer','Additional info about EditionServer','Additional info about EditionServer','Additional info about EditionServer','Additional info about EditionServer','Additional info about EditionServer','Additional info about EditionServer','Additional info about EditionServer','Additional info about EditionServer','Additional info about EditionServer','Additional info about EditionServer','Additional info about EditionServer','Additional info about EditionServer','Additional info about EditionServer','Additional info about EditionServer'
    ]

    editions = Edition.objects.all().values_list('id', flat=True)
    servers = Server.objects.all().values_list('id', flat=True)

    edition_server_edition_ids = [editions[0], editions[1], editions[2], editions[3], editions[4], editions[5], editions[6], editions[7], editions[8], editions[9], editions[10], editions[11], editions[12], editions[13], editions[14], editions[15]]
    edition_server_server_ids = [servers[2], servers[0], servers[3], servers[4], servers[2], servers[0], servers[3], servers[4], servers[2], servers[0], servers[3], servers[4], servers[2], servers[0], servers[3], servers[4]]

    for i in range(len(edition_server_add_info)):
        EditionServer.objects.using(db_alias).create(
            additional_info=edition_server_add_info[i], edition_id=edition_server_edition_ids[i], server_id=edition_server_server_ids[i]
    )

    teachers = Teacher.objects.all().values_list('id', flat=True)

    teacher_edition_edition_id = [editions[0], editions[1], editions[2], editions[3], editions[4], editions[5], editions[6], editions[7], editions[8], editions[9], editions[10], editions[11], editions[12], editions[13], editions[14], editions[15]]
    teacher_edition_teacher_id = [teachers[0], teachers[1], teachers[2], teachers[3], teachers[0], teachers[1], teachers[2], teachers[3], teachers[0], teachers[1], teachers[2], teachers[3], teachers[0], teachers[1], teachers[2], teachers[3]]

    for i in range(len(teacher_edition_edition_id)):
        TeacherEdition.objects.using(db_alias).create(
            edition_id=teacher_edition_edition_id[i], teacher_id=teacher_edition_teacher_id[i]
    )

    group_names = ['L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7', 'L8', 'L9', 'L10', 'L11', 'L12', 'L13', 'L14']
    group_days = ['Poniedziałek', 'Środa', 'Wtorek', 'Poniedziałek', 'Wtorek', 'Piątek', 'Czwartek', 'Poniedziałek', 'Środa', 'Piątek', 'Wtorek', 'Środa', 'Czwartek', 'Poniedziałek']
    group_hours = ['11:45', '8:00', '8:00', '9:45', '13:30', '16:50', '13:30', '11:45', '15:10', '8:00', '8:00', '9:45', '11:45', '13:30']
    group_rooms = ['1.6.18', 'CW 8', '2.2.2', 'CW 9', '1.5.5', 'A6', '1.4.4', '2.2.2', '1.2.2', '2.2.2', '1.1.1', '4.4.4', '2.2.2', '1.1.1']

    teacher_editions = TeacherEdition.objects.all()
    students_all = Student.objects.all()

    for i in range(len(group_names)):
        created_group = Group.objects.using(db_alias).create(
            name=group_names[i], day=group_days[i], hour=group_hours[i], room=group_rooms[i], teacherEdition=teacher_editions[i]
        )
        for j in range(i * 6, i * 6 + 6):
            created_group.students.add(students_all[j])

    L1_L2_edition_servers = [0,5,10,15]
    L3_L4_edition_servers = [1,6,11]
    L5_L6_edition_servers = [2,7]
    L7_L8_edition_servers = [3]
    L9_L10_edition_servers = [4,9,14]
    L11_L12_edition_servers = [8,13]
    L13_L14_edition_servers = [12]

    edition_servers = EditionServer.objects.all()

    for i in range(10, len(users_names)):
        if 0 <= i <= 11: # L1 L2
            for j in range(len(L1_L2_edition_servers)):
                DBAccount.objects.using(db_alias).create(
                    username=users_names[i].split()[1] + '-dbusername', password=users_names[i].split()[1] + '-dbpassword', additional_info="Additional info about dbaccount", isMovedToExtDB=False, student=students_all[i-10], editionServer=edition_servers[j]
            )
        if 12 <= i <= 23: # L3 L4
            for j in range(len(L3_L4_edition_servers)):
                DBAccount.objects.using(db_alias).create(
                    username=users_names[i].split()[1] + '-dbusername', password=users_names[i].split()[1] + '-dbpassword', additional_info="Additional info about dbaccount", isMovedToExtDB=False, student=students_all[i-10], editionServer=edition_servers[j]
            )
        if 24 <= i <= 35: # L5 L6
            for j in range(len(L5_L6_edition_servers)):
                DBAccount.objects.using(db_alias).create(
                    username=users_names[i].split()[1] + '-dbusername', password=users_names[i].split()[1] + '-dbpassword', additional_info="Additional info about dbaccount", isMovedToExtDB=False, student=students_all[i-10], editionServer=edition_servers[j]
            )
        if 36 <= i <= 47: # L7 L8
            for j in range(len(L7_L8_edition_servers)):
                DBAccount.objects.using(db_alias).create(
                    username=users_names[i].split()[1] + '-dbusername', password=users_names[i].split()[1] + '-dbpassword', additional_info="Additional info about dbaccount", isMovedToExtDB=False, student=students_all[i-10], editionServer=edition_servers[j]
            )
        if 48 <= i <= 59: # L9 L10
            for j in range(len(L9_L10_edition_servers)):
                DBAccount.objects.using(db_alias).create(
                    username=users_names[i].split()[1] + '-dbusername', password=users_names[i].split()[1] + '-dbpassword', additional_info="Additional info about dbaccount", isMovedToExtDB=False, student=students_all[i-10], editionServer=edition_servers[j]
            )
        if 60 <= i <= 71: # L11 L12
            for j in range(len(L11_L12_edition_servers)):
                DBAccount.objects.using(db_alias).create(
                    username=users_names[i].split()[1] + '-dbusername', password=users_names[i].split()[1] + '-dbpassword', additional_info="Additional info about dbaccount", isMovedToExtDB=False, student=students_all[i-10], editionServer=edition_servers[j]
            )
        if 72 <= i <= 83: # L13 L14
            for j in range(len(L13_L14_edition_servers)):
                DBAccount.objects.using(db_alias).create(
                    username=users_names[i].split()[1] + '-dbusername', password=users_names[i].split()[1] + '-dbpassword', additional_info="Additional info about dbaccount", isMovedToExtDB=False, student=students_all[i-10], editionServer=edition_servers[j]
            )


    



class Migration(migrations.Migration):

    dependencies = [
        ('database', '0003_alter_course_description_alter_dbaccount_student_and_more'),
        # ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.RunPython(forwards_func),
        # migrations.RunSQL(
        #     sql="""
        #         delete from database_dbaccount;
        #         delete from database_studentgroup;
        #         delete from database_group;
        #         delete from database_teacheredition;
        #         delete from database_editionserver;
        #         delete from database_edition;
        #         delete from database_teacher;
        #         delete from database_student;
        #         delete from database_admin;
        #         delete from database_user;
        #         delete from database_semester;
        #         delete from database_course;
        #         delete from database_server;

        #         INSERT INTO public.database_server
        #         (id, "name", ip, port, date_created, active)
        #         VALUES(1, 'POSTGRES', '150.24.150.30', 5432, '2017-08-09', true);
        #         INSERT INTO public.database_server
        #         (id, "name", ip, port, date_created, active)
        #         VALUES(2, 'MYSQL', '170.225.225.225', 1234, '2015-04-06', true);
        #         INSERT INTO public.database_server
        #         (id, "name", ip, port, date_created, active)
        #         VALUES(3, 'MONGO_DB', '155.155.200.205', 3333, '2019-05-11', false);
        #         INSERT INTO public.database_server
        #         (id, "name", ip, port, date_created, active)
        #         VALUES(4, 'CASSANDRA', '120.120.255.255', 1234, '2016-01-04', true);
        #         INSERT INTO public.database_server
        #         (id, "name", ip, port, date_created, active)
        #         VALUES(5, 'ORACLE', '111.111.120.125', 1111, '2022-12-12', false);
        #         INSERT INTO public.database_server
        #         (id, "name", ip, port, date_created, active)
        #         VALUES(6, 'ORACLE_NEW', '111.111.120.145', 2537, '2023-05-08', true);



        #         INSERT INTO public.database_course
        #         (id, "name", description)
        #         VALUES(1, 'Zarządzanie bazami danych', 'Kurs zarządzania bazami danych SQL i noSQL');
        #         INSERT INTO public.database_course
        #         (id, "name", description)
        #         VALUES(2, 'Podstawy baz danych', 'Kurs podstaw baz danych');
        #         INSERT INTO public.database_course
        #         (id, "name", description)
        #         VALUES(3, 'Administacja baz danych', 'Kurs administrowania baz danych');
        #         INSERT INTO public.database_course
        #         (id, "name", description)
        #         VALUES(4, 'Projektowanie baz danych', 'Kurs projektowania baz danych');
        #         INSERT INTO public.database_course
        #         (id, "name", description)
        #         VALUES(5, 'Zaawansowane bazy danych', 'Kurs zaawansowany baz danych');


        #         INSERT INTO public.database_semester
        #         (id, "year", winter)
        #         VALUES(1, '2020/2021', true);
        #         INSERT INTO public.database_semester
        #         (id, "year", winter)
        #         VALUES(2, '2017/2018', false);
        #         INSERT INTO public.database_semester
        #         (id, "year", winter)
        #         VALUES(3, '2019/2020', true);
        #         INSERT INTO public.database_semester
        #         (id, "year", winter)
        #         VALUES(4, '2019/2020', false);
        #         INSERT INTO public.database_semester
        #         (id, "year", winter)
        #         VALUES(5, '2022/2023', true);



        #         INSERT INTO public.database_user
        #         (id, first_name, last_name, email, "password", polymorphic_ctype_id)
        #         VALUES(2, 'Jakub', 'Wrobel', 'jakub.p.wrobel@student.put.poznan.pl', 'haslojakuba', 15);
        #         INSERT INTO public.database_user
        #         (id, first_name, last_name, email, "password", polymorphic_ctype_id)
        #         VALUES(3, 'Krystian', 'Jakusik', 'krystian.jakusik@student.put.poznan.pl', 'krystian123', 15);
        #         INSERT INTO public.database_user
        #         (id, first_name, last_name, email, "password", polymorphic_ctype_id)
        #         VALUES(4, 'Przemysław', 'Woźniak', 'przemyslaw.wozniak@student.put.poznan.pl', 'przemekwprzemek', 15);
        #         INSERT INTO public.database_user
        #         (id, first_name, last_name, email, "password", polymorphic_ctype_id)
        #         VALUES(5, 'Bartosz', 'Bębel', 'bartosz.bebel@cs.put.poznan.pl', 'Bartosz', 14);
        #         INSERT INTO public.database_user
        #         (id, first_name, last_name, email, "password", polymorphic_ctype_id)
        #         VALUES(6, 'Michał', 'Apolinarski', 'michal.apolinarski@cs.put.poznan.pl', 'michalapol123', 16);
        #         INSERT INTO public.database_user
        #         (id, first_name, last_name, email, "password", polymorphic_ctype_id)
        #         VALUES(7, 'Jan', 'Kowalski', 'jan.kowalski@student.put.poznan.pl', 'jkowal', 15);
        #         INSERT INTO public.database_user
        #         (id, first_name, last_name, email, "password", polymorphic_ctype_id)
        #         VALUES(8, 'Michał', 'Nowak', 'michal.t.nowak@student.put.poznan.pl', 'nowakkk', 15);
        #         INSERT INTO public.database_user
        #         (id, first_name, last_name, email, "password", polymorphic_ctype_id)
        #         VALUES(9, 'Arkadiusz', 'Instruktor', 'arkadiusz.instruktor@cs.put.poznan.pl', 'arekins', 14);
        #         INSERT INTO public.database_user
        #         (id, first_name, last_name, email, "password", polymorphic_ctype_id)
        #         VALUES(10, 'Tomasz', 'Nauczycielski', 'tomasz.nauczycielski@cs.put.poznan.pl', 'tomnau', 16);
        #         INSERT INTO public.database_user
        #         (id, first_name, last_name, email, "password", polymorphic_ctype_id)
        #         VALUES(11, 'Wiktor', 'Wykładnik', 'wiktor.wykładnik@cs.put.poznan.pl', 'potega123', 16);
        #         INSERT INTO public.database_user
        #         (id, first_name, last_name, email, "password", polymorphic_ctype_id)
        #         VALUES(12, 'Konrad', 'Indeksowy', 'konrad.indeksowy@cs.put.poznan.pl', 'indeksik213', 16);



        #         INSERT INTO public.database_admin
        #         (user_ptr_id)
        #         VALUES(5);
        #         INSERT INTO public.database_admin
        #         (user_ptr_id)
        #         VALUES(9);


        #         INSERT INTO public.database_student
        #         (user_ptr_id, student_id)
        #         VALUES(2, '145188');
        #         INSERT INTO public.database_student
        #         (user_ptr_id, student_id)
        #         VALUES(3, '145318');
        #         INSERT INTO public.database_student
        #         (user_ptr_id, student_id)
        #         VALUES(4, '145423');
        #         INSERT INTO public.database_student
        #         (user_ptr_id, student_id)
        #         VALUES(7, '145222');
        #         INSERT INTO public.database_student
        #         (user_ptr_id, student_id)
        #         VALUES(8, '145111');


        #         INSERT INTO public.database_teacher
        #         (user_ptr_id)
        #         VALUES(6);
        #         INSERT INTO public.database_teacher
        #         (user_ptr_id)
        #         VALUES(10);
        #         INSERT INTO public.database_teacher
        #         (user_ptr_id)
        #         VALUES(11);
        #         INSERT INTO public.database_teacher
        #         (user_ptr_id)
        #         VALUES(12);



        #         INSERT INTO public.database_edition
        #         (id, description, date_opened, date_closed, active, course_id, semester_id)
        #         VALUES(1, '-', '2019-01-09', '2020-01-03', false, 1, 2);
        #         INSERT INTO public.database_edition
        #         (id, description, date_opened, date_closed, active, course_id, semester_id)
        #         VALUES(2, '-', '2022-01-10', '2023-01-03', true, 2, 3);
        #         INSERT INTO public.database_edition
        #         (id, description, date_opened, date_closed, active, course_id, semester_id)
        #         VALUES(3, '-', '2023-01-08', '2023-01-01', true, 3, 3);
        #         INSERT INTO public.database_edition
        #         (id, description, date_opened, date_closed, active, course_id, semester_id)
        #         VALUES(4, '-', '2012-01-01', '2016-01-01', false, 4, 4);



        #         INSERT INTO public.database_editionserver
        #         (id, additional_info, edition_id, server_id)
        #         VALUES(1, 'Additional info about server 1', 1, 1);
        #         INSERT INTO public.database_editionserver
        #         (id, additional_info, edition_id, server_id)
        #         VALUES(2, 'Additional info about server 2', 2, 2);
        #         INSERT INTO public.database_editionserver
        #         (id, additional_info, edition_id, server_id)
        #         VALUES(3, 'Additional info about server 3', 4, 1);
        #         INSERT INTO public.database_editionserver
        #         (id, additional_info, edition_id, server_id)
        #         VALUES(4, 'Additional info about server 4', 3, 2);



        #         INSERT INTO public.database_teacheredition
        #         (id, edition_id, teacher_id)
        #         VALUES(1, 1, 6);
        #         INSERT INTO public.database_teacheredition
        #         (id, edition_id, teacher_id)
        #         VALUES(2, 2, 6);
        #         INSERT INTO public.database_teacheredition
        #         (id, edition_id, teacher_id)
        #         VALUES(3, 2, 10);
        #         INSERT INTO public.database_teacheredition
        #         (id, edition_id, teacher_id)
        #         VALUES(4, 3, 10);
        #         INSERT INTO public.database_teacheredition
        #         (id, edition_id, teacher_id)
        #         VALUES(5, 3, 11);
        #         INSERT INTO public.database_teacheredition
        #         (id, edition_id, teacher_id)
        #         VALUES(6, 4, 12);



        #         INSERT INTO public.database_group
        #         (id, "name", "day", "hour", room, "teacherEdition_id")
        #         VALUES(1, 'L10', 'Monday', '11:45', '3a', 1);
        #         INSERT INTO public.database_group
        #         (id, "name", "day", "hour", room, "teacherEdition_id")
        #         VALUES(2, 'L5', 'Tuesday', '13:30', '11b', 2);
        #         INSERT INTO public.database_group
        #         (id, "name", "day", "hour", room, "teacherEdition_id")
        #         VALUES(3, 'L1', 'Friday', '10:00', '1', 3);
        #         INSERT INTO public.database_group
        #         (id, "name", "day", "hour", room, "teacherEdition_id")
        #         VALUES(4, 'L2', 'Thursday', '12:00', '2', 4);
        #         INSERT INTO public.database_group
        #         (id, "name", "day", "hour", room, "teacherEdition_id")
        #         VALUES(5, 'L3', 'Wednesday', '11:00', '3', 5);
        #         INSERT INTO public.database_group
        #         (id, "name", "day", "hour", room, "teacherEdition_id")
        #         VALUES(6, 'L4', 'Monday', '10:00', '4', 6);



        #         INSERT INTO public.database_studentgroup
        #         (id, group_id, student_id)
        #         VALUES(1, 1, 3);
        #         INSERT INTO public.database_studentgroup
        #         (id, group_id, student_id)
        #         VALUES(2, 2, 4);
        #         INSERT INTO public.database_studentgroup
        #         (id, group_id, student_id)
        #         VALUES(3, 1, 2);
        #         INSERT INTO public.database_studentgroup
        #         (id, group_id, student_id)
        #         VALUES(4, 3, 7);
        #         INSERT INTO public.database_studentgroup
        #         (id, group_id, student_id)
        #         VALUES(5, 4, 8);



        #         INSERT INTO public.database_dbaccount
        #         (id, username, "password", additional_info, "editionServer_id", student_id)
        #         VALUES(1, 'jwrobel', 'inf145188', 'Additional info about user id 1', 1, 2);
        #         INSERT INTO public.database_dbaccount
        #         (id, username, "password", additional_info, "editionServer_id", student_id)
        #         VALUES(2, 'pwozniak', 'inf145423', 'Additional info about user id 2', 2, 3);
        #         INSERT INTO public.database_dbaccount
        #         (id, username, "password", additional_info, "editionServer_id", student_id)
        #         VALUES(3, 'kjakusik', 'inf145318', 'Additional info about user id 3', 1, 4);
        #         INSERT INTO public.database_dbaccount
        #         (id, username, "password", additional_info, "editionServer_id", student_id)
        #         VALUES(4, 'jkowal', 'inf145111', 'Additional info about user id 4', 3, 7);
        #         INSERT INTO public.database_dbaccount
        #         (id, username, "password", additional_info, "editionServer_id", student_id)
        #         VALUES(5, 'mnowak', 'inf145222', 'Additional info about user id 5', 4, 8);
        #         """
                # )
                ]