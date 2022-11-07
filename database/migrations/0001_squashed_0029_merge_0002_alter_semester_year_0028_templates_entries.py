# Generated by Django 4.0.5 on 2022-10-21 12:58

from django.db import migrations, models
import django.db.models.deletion


# Functions from the following migrations need manual copying.
# Move them and any dependencies into this file, then update the
# RunPython operations to refer to the local versions:
# database.migrations.0028_templates_entries


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
    admin_ct = ContentType.objects.get_for_model(Admin)

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

    server_names = ['MySQL ZBD Server', 'Oracle ZBD Server - OFFLINE', 'Postgres PBD Server', 'Mongo ZBDNS Server', 'Microsoft SQL Server PBD']
    server_ipss = ['localhost', '128.127.80.0', 'localhost', '156.154.84.0', '176.119.32.0']
    server_ports = ['3306', '5432', '5433', '2850', '4179']
    server_date_createds = '2021-12-31'
    server_actives = [True, False, True, True, True]
    server_databases = ['mysql', 'oracledb', 'postgres', 'mongodbnosql', 'mssql']
    server_passwords = ['root', 'oracledbpass', 'postgrespass', 'mongodbnosqlpass', 'mssqlpass']
    server_providers = ['MySQL', 'Oracle', 'Postgres', 'MongoDB', 'Microsoft SQL Server']
    server_users = ['root', 'oracledbuser', 'postgresuser', 'mongodbnosqluser', 'mssqluser']
    server_create_user_templates = ["CREATE USER IF NOT EXISTS %s@'localhost' IDENTIFIED BY %s;", ' ', "CREATE USER \"%s\" WITH PASSWORD \'%s\';", ' ', ' ']

    for i in range(len(server_names)):
        Server.objects.using(db_alias).create(
        name=server_names[i], ip=server_ipss[i], port=server_ports[i], date_created=server_date_createds, active=server_actives[i], database=server_databases[i], password=server_passwords[i], provider=server_providers[i], user=server_users[i], create_user_template=server_create_user_templates[i]
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

    Admin.objects.using(db_alias).create(
        first_name="Admin", last_name="Admin", email='admin@cs.put.poznan.pl' , password='admin123', polymorphic_ctype_id=admin_ct.id
    )

    for i in range(10):
        Teacher.objects.using(db_alias).create(
            first_name=users_names[i].split()[0], last_name=users_names[i].split()[1], email=users_names[i].split()[0] + '.' + users_names[i].split()[1] + '@cs.put.poznan.pl' , password=users_names[i].split()[1] + '123', polymorphic_ctype_id=teacher_ct.id
        )

    for i in range(11, len(users_names)):
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

    edition_server_username_templates = [
        "INF_{NR_INDEKSU}", '{IMIE} + { NAZWISKO}', '{NAZWISKO}_{NUMER_INDEKSU}', 'STUDENT_{NUMBER_INDEKSU}', "INF_{NR_INDEKSU}", '{IMIE} + { NAZWISKO}', '{NAZWISKO}_{NUMER_INDEKSU}', 'STUDENT_{NUMBER_INDEKSU}', "INF_{NR_INDEKSU}", '{IMIE} + { NAZWISKO}', '{NAZWISKO}_{NUMER_INDEKSU}', 'STUDENT_{NUMBER_INDEKSU}', "INF_{NR_INDEKSU}", '{IMIE} + { NAZWISKO}', '{NAZWISKO}_{NUMER_INDEKSU}', 'STUDENT_{NUMBER_INDEKSU}'
    ]

    edition_server_passwd_templates = [
        "blank", "default_passwd", "123", "inf{NR_INDEKSU}", "blank", "default_passwd", "123", "inf{NR_INDEKSU}", "blank", "default_passwd", "123", "inf{NR_INDEKSU}", "blank", "default_passwd", "123", "inf{NR_INDEKSU}"
    ]


    editions = Edition.objects.all().values_list('id', flat=True)
    servers = Server.objects.all().values_list('id', flat=True)

    edition_server_edition_ids = [editions[0], editions[1], editions[2], editions[3], editions[4], editions[5], editions[6], editions[7], editions[8], editions[9], editions[10], editions[11], editions[12], editions[13], editions[14], editions[15]]
    edition_server_server_ids = [servers[2], servers[0], servers[3], servers[4], servers[2], servers[0], servers[3], servers[4], servers[2], servers[0], servers[3], servers[4], servers[2], servers[0], servers[3], servers[4]]

    for i in range(len(edition_server_add_info)):
        EditionServer.objects.using(db_alias).create(
            additional_info=edition_server_add_info[i], edition_id=edition_server_edition_ids[i], server_id=edition_server_server_ids[i], username_template=edition_server_username_templates[i], passwd_template=edition_server_passwd_templates[i]
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
                    username=students_all[i-10].last_name + '-dbusername', password=students_all[i-10].last_name + '-dbpassword', additional_info="Additional info about dbaccount", is_moved=False, student=students_all[i-10], editionServer=edition_servers[j]
            )
        if 12 <= i <= 23: # L3 L4
            for j in range(len(L3_L4_edition_servers)):
                DBAccount.objects.using(db_alias).create(
                    username=students_all[i-10].last_name + '-dbusername', password=students_all[i-10].last_name + '-dbpassword', additional_info="Additional info about dbaccount", is_moved=False, student=students_all[i-10], editionServer=edition_servers[j]
            )
        if 24 <= i <= 35: # L5 L6
            for j in range(len(L5_L6_edition_servers)):
                DBAccount.objects.using(db_alias).create(
                    username=students_all[i-10].last_name + '-dbusername', password=students_all[i-10].last_name + '-dbpassword', additional_info="Additional info about dbaccount", is_moved=False, student=students_all[i-10], editionServer=edition_servers[j]
            )
        if 36 <= i <= 47: # L7 L8
            for j in range(len(L7_L8_edition_servers)):
                DBAccount.objects.using(db_alias).create(
                    username=students_all[i-10].last_name + '-dbusername', password=students_all[i-10].last_name + '-dbpassword', additional_info="Additional info about dbaccount", is_moved=False, student=students_all[i-10], editionServer=edition_servers[j]
            )
        if 48 <= i <= 59: # L9 L10
            for j in range(len(L9_L10_edition_servers)):
                DBAccount.objects.using(db_alias).create(
                    username=students_all[i-10].last_name + '-dbusername', password=students_all[i-10].last_name + '-dbpassword', additional_info="Additional info about dbaccount", is_moved=False, student=students_all[i-10], editionServer=edition_servers[j]
            )
        if 60 <= i <= 71: # L11 L12
            for j in range(len(L11_L12_edition_servers)):
                DBAccount.objects.using(db_alias).create(
                    username=students_all[i-10].last_name + '-dbusername', password=students_all[i-10].last_name + '-dbpassword', additional_info="Additional info about dbaccount", is_moved=False, student=students_all[i-10], editionServer=edition_servers[j]
            )
        if 72 <= i <= 83: # L13 L14
            for j in range(len(L13_L14_edition_servers)):
                DBAccount.objects.using(db_alias).create(
                    username=students_all[i-10].last_name + '-dbusername', password=students_all[i-10].last_name + '-dbpassword', additional_info="Additional info about dbaccount", is_moved=False, student=students_all[i-10], editionServer=edition_servers[j]
            )

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('description', models.CharField(blank=True, default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Edition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=100)),
                ('date_opened', models.DateField()),
                ('date_closed', models.DateField()),
                ('active', models.BooleanField(default=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.course')),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('description', models.CharField(blank=True, default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(max_length=9)),
                ('winter', models.BooleanField(default=True)),
                ('active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('ip', models.CharField(max_length=30)),
                ('port', models.CharField(max_length=10)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=30)),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_%(app_label)s.%(class)s_set+', to='contenttypes.contenttype')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='database.user')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('database.user',),
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='database.user')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('database.user',),
        ),
        migrations.CreateModel(
            name='TeacherEdition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('edition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.edition')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='EditionServer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('additional_info', models.CharField(blank=True, default='', max_length=255)),
                ('edition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.edition')),
                ('server', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.server')),
                ('passwd_template', models.CharField(max_length=255, null=True)),
                ('username_template', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='edition',
            name='semester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='editions', to='database.semester'),
        ),
        migrations.RemoveField(
            model_name='edition',
            name='name',
        ),
        migrations.AlterField(
            model_name='edition',
            name='date_closed',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='edition',
            name='date_opened',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='edition',
            name='teachers',
            field=models.ManyToManyField(blank=True, related_name='editions', through='database.TeacherEdition', to='database.teacher'),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='database.user')),
                ('student_id', models.CharField(max_length=6, unique=True)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('database.user',),
        ),
        migrations.AddField(
            model_name='server',
            name='edition',
            field=models.ManyToManyField(related_name='servers', through='database.EditionServer', to='database.edition'),
        ),
        migrations.AlterField(
            model_name='edition',
            name='description',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('day', models.CharField(blank=True, default='', max_length=30)),
                ('hour', models.CharField(blank=True, default='', max_length=30)),
                ('room', models.CharField(blank=True, default='', max_length=30)),
                ('teacherEdition', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='database.teacheredition')),
                ('students', models.ManyToManyField(related_name='groups', to='database.student')),
            ],
        ),
        migrations.AddField(
            model_name='server',
            name='database',
            field=models.CharField(max_length=30),
        ),
        migrations.AddField(
            model_name='server',
            name='password',
            field=models.CharField(max_length=30),
        ),
        migrations.AddField(
            model_name='server',
            name='provider',
            field=models.CharField(max_length=30),
        ),
        migrations.AddField(
            model_name='server',
            name='user',
            field=models.CharField(max_length=30),
        ),
        migrations.CreateModel(
            name='Major',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('description', models.CharField(blank=True, default='', max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='major',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='courses', to='database.major'),
        ),
        migrations.CreateModel(
            name='DBAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
                ('additional_info', models.CharField(blank=True, default='', max_length=255)),
                ('editionServer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='database.editionserver')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='db_accounts', to='database.student')),
                ('is_moved', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('description', models.CharField(blank=True, default='', max_length=100)),
                ('permisssions', models.ManyToManyField(blank=True, related_name='roles', to='database.permission')),
                ('users', models.ManyToManyField(blank=True, related_name='roles', to='database.user')),
            ],
        ),
        migrations.AlterField(
            model_name='edition',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='editions', to='database.course'),
        ),
            migrations.AddField(
            model_name='server',
            name='create_user_template',
            field=models.CharField(max_length=100),
        ),
        migrations.RunPython(forwards_func),
        migrations.AlterField(
            model_name='semester',
            name='year',
            field=models.CharField(max_length=9),
        ),
    ]
