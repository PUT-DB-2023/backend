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
    Major = apps.get_model('database', 'Major')
    

    
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
    Major.objects.all().delete()
    Server.objects.all().delete()

    

    server_names = ['MySQL ZBD Server', 'Oracle ZBD Server', 'Postgres PBD Server', 'Mongo ZBDNS Server', 'Microsoft SQL Server PBD']
    server_ipss = ['185.180.207.251', '185.150.207.251', '185.180.207.251', 'mongo', '176.119.32.0']
    # server_ports = ['3306', '5432', '5433', '2850', '4179']
    # server_ipss = ['localhost', '128.127.80.0', 'postgres-external', '156.154.84.0', '176.119.32.0']
    server_ports = ['3306', '44475', '5432', '27017', '4179']
    server_date_createds = '2021-12-31'
    server_databases = ['mysql', 'xe', 'postgres', 'database', 'mssql']
    server_passwords = ['mysql12', 'PASSWORD', 'postgres12', 'mongo12', 'mssqlpass']
    # server_passwords = ['root', 'oracledbpass', 'postgres', 'mongodbnosqlpass', 'mssqlpass']
    server_providers = ['MySQL', 'Oracle', 'Postgres', 'MongoDB', 'Microsoft SQL Server']
    server_users = ['root', 'USERDB', 'postgres', 'root', 'mssqluser']
    server_create_user_templates = ["CREATE USER IF NOT EXISTS \"%s\"@'%%' IDENTIFIED BY '%s'", "", "CREATE USER \"%s\" WITH PASSWORD \'%s\';", '"createUser" : %s, "pwd" : %s, "customData" : {}, "roles" : []', ""]
    server_modify_user_templates = ["ALTER USER %s@'localhost' IDENTIFIED BY %s;", "", "ALTER USER \"%s\" WITH PASSWORD \'%s\';", "", ""]
    server_delete_user_templates = ["DROP USER IF EXISTS \"%s\"@'%%';", "", "DROP USER IF EXISTS \"%s\";", "", ""]

    for i in range(len(server_names)):
        Server.objects.using(db_alias).create(
        name=server_names[i], ip=server_ipss[i], port=server_ports[i], date_created=server_date_createds, database=server_databases[i], password=server_passwords[i], provider=server_providers[i], user=server_users[i], create_user_template=server_create_user_templates[i],
        modify_user_template=server_modify_user_templates[i], delete_user_template=server_delete_user_templates[i]
    )

    major_names = ['Informatyka', 'Automatyka i Robotyka']
    major_description = ['Opis kierunku Informatyka', 'Opis kierunku Automatyka i Robotyka']

    for i in range(len(major_names)):
        Major.objects.using(db_alias).create(
        name=major_names[i], description=major_description[i]
    )

    course_names = ['Zarządzanie bazami danych', 'Podstawy baz danych', 'Zarządzanie bazami NoSQL', 'Projektowanie baz danych']
    course_descriptions = ['Opis kursu zarządzania bazami danych', 'Opis kursu podstaw baz danych', 'Opis kursu zarządzania bazami danych noSQL', 'Opis kursu projektowania baz danych']
    course_active = [True, True, True, False]
    course_major = [Major.objects.get(name='Informatyka'), Major.objects.get(name='Informatyka'), Major.objects.get(name='Automatyka i Robotyka'), Major.objects.get(name='Informatyka')]

    for i in range(len(course_names)):
        Course.objects.using(db_alias).create(
            name=course_names[i], description=course_descriptions[i], active=course_active[i], major=course_major[i]
    )

    semester_years = ['2021/2022', '2022/2023']
    semester_winters = [True, True]
    semester_actives = [False, True]

    for i in range(len(semester_years)):
        Semester.objects.using(db_alias).create(
            year=semester_years[i], winter=semester_winters[i], active=semester_actives[i]
    )

    users_names = ["Ferdynand Dulski","Celestyn Tomaszewski","Sylwester Kaczkowski","Juri Rokicki","Pabian Archacki","Leo Zelek","Kwiatosław Greger","Hubert Kiedrowski","Waldemar Piotrowicz","Olaf Gursky","Hilary Franczak","Melchior Perzan","Świętosław Kopa","Marcin Gorniak","Oskar Kobylinski","Tymon Bialek","Gabriel Orlowski","Pankracy Grodzicki","Serwacy Watroba","Zygmunt Bilik","Aleksander Nabozny","Maryn Wyszynski","Remigiusz Ciolek","Cyprian Gracyalny","Dominik Bernacki","Szymon Rogalski","Ignacy Smigel","Ireneusz Dziak","Wisław Gielgud","Korneli Krynicki","Świętosław Lozowski","Bartłomiej Lach","Konstantyn Pitera","Franciszek Sochaczewski","Malachiasz Car","Eugeniusz Jaracz","Zbigniew Kula","Kamil Rajewski","Zenon Kosmalski","Chwalimir Bania","Romuald Mita","Ryszard Nowak","Sławomir Garstka","Tomasz Kocik","Gerwazy Cieply","Gwalbert Grodzicki","Denis Slusarczyk","Edward Przybylowicz","Malachiasz Cesarz","Iwon Capek","Dobrogost Wojtaszek","Świętosław Pawelski","Tobiasz Raczkowski","Gerard Chmiel","Bartosz Burak","Oktawiusz Ignasiak","Arkadiusz Michalak","Zdzisław Luka","Jerzy Kurcz","Julian Karczewski","Herbert Marcinkiewicz","Klemens Krzyzaniak","Metody Mioduszewski","Gościsław Niziolek","Sylwester Kaczkowski","Fryderyk Dusza","Dobrogost Wójcik","Albin Bialy","Jaromir Misiaszek","Tadeusz Galik","Bożidar Jablon","Witold Demby","Chrystian Krolikowski","Kryspyn Piekarz","Nikodem Czepiec","Wojsław Korczak","Hugo Tylka","Lubomił Ciesinski","Wisław Samborski","Bożimir Jagodzinski","Hilary Lesak","Adrian Bartel","Prot Ewy","Ludomił Kaniuk","Dobrogost Syslo","Adrian Dudzinski","Florentyn Rawski","Bożimir Banik","Wandelin Jaroszewski","Herbert Pekala","Gustaw Dobek","Oskar Jusko","Maksymilian Zajac","Bronisław Prus","Marcel Zaczek","Antoni Wiech","Przemysław Woźniak","Jakub Wróbel","Krystian Jakusik","Kamil Ambozy"]

    Admin.objects.using(db_alias).create(
        first_name="Admin", last_name="Admin", email='admin@cs.put.poznan.pl' , password='admin123', polymorphic_ctype_id=admin_ct.id
    )

    for i in range(4):
        Teacher.objects.using(db_alias).create(
            first_name=users_names[i].split()[0], last_name=users_names[i].split()[1], email=users_names[i].split()[0] + '.' + users_names[i].split()[1] + '@cs.put.poznan.pl' , password=users_names[i].split()[1] + '123', polymorphic_ctype_id=teacher_ct.id
        )

    for i in range(4, len(users_names)):
        Student.objects.using(db_alias).create(
            first_name=users_names[i].split()[0], last_name=users_names[i].split()[1], email=users_names[i].split()[0] + '.' + users_names[i].split()[1] + '@student.put.poznan.pl' , password=users_names[i].split()[1] + '123', student_id=str(100000+i), polymorphic_ctype_id=student_ct.id
        )

    edition_descriptions = [
        'Edycja 2022/2023 kursu Podstawy baz danych','Edycja 2022/2023 kursu Zarządzanie bazami danych', 'Edycja 2022/2023 kursu Zarządzanie bazami danych noSQL', 'Edycja 2021/2022 kursu Projektowanie baz danych'
        ]

    dates_opened = ['2019-10-01' for _ in range(8)]

    dates_closed = [
        None, None, None, '2022-06-30'
    ]

    courses = Course.objects.all().values_list('id', flat=True)

    courses_ids = [courses[1], courses[0], courses[2], courses[3]]

    semesters = Semester.objects.all().values_list('id', flat=True)

    semestres_ids = [
        semesters[1], semesters[1], semesters[1], semesters[0],
    ]

    for i in range(len(edition_descriptions)):
        Edition.objects.using(db_alias).create(
            description=edition_descriptions[i], date_opened=dates_opened[i], date_closed=dates_closed[i], course_id=courses_ids[i], semester_id=semestres_ids[i]
    )

    edition_server_add_info = ['Additional info about EditionServer' for _ in range(4)]

    edition_server_username_templates = [
        "INF_{NR_INDEKSU}", '{IMIE} + {NAZWISKO}', '{NAZWISKO}_{NR_INDEKSU}', 'STUDENT_{NR_INDEKSU}'
    ]

    edition_server_passwd_templates = [
        "blank", "default_passwd", "123", "inf{NR_INDEKSU}"
    ]

    editions = Edition.objects.all().values_list('id', flat=True)
    servers = Server.objects.all().values_list('id', flat=True)

    edition_server_edition_ids = [editions[i] for i in range(4)]
    edition_server_server_ids = [servers[2], servers[0], servers[3], servers[1]]

    for i in range(len(edition_server_add_info)):
        EditionServer.objects.using(db_alias).create(
            additional_info=edition_server_add_info[i], edition_id=edition_server_edition_ids[i], server_id=edition_server_server_ids[i], username_template=edition_server_username_templates[i], passwd_template=edition_server_passwd_templates[i]
    )

    # special edition server so that one edition has two servers
    EditionServer.objects.using(db_alias).create(
        additional_info='Additional info about EditionServer', edition_id=editions[0], server_id=servers[0], username_template='INF_{NR_INDEKSU}', passwd_template='blank'
    )

    teachers = Teacher.objects.all().values_list('id', flat=True)

    teacher_edition_edition_id = [editions[i] for i in range(4)]
    teacher_edition_teacher_id = [teachers[0], teachers[1], teachers[2], teachers[3]]

    for i in range(len(teacher_edition_edition_id)):
        TeacherEdition.objects.using(db_alias).create(
            edition_id=teacher_edition_edition_id[i], teacher_id=teacher_edition_teacher_id[i]
    )

    group_names = ['Grupa 1 ZBD', 'Grupa 2 ZBD', 'Grupa 3 ZBD', 'Grupa 4 PBD', 'Grupa 5 PBD', 'Grupa 6 PBD', 'Grupa 7 ZBN', 'Grupa 8 ZBN', 'Grupa 9 ZBN', 'Grupa 10 ProjBD - NA', 'Grupa 11 ProjBD - NA', 'Grupa 12 ProjBD - NA']
    group_days = ['Poniedziałek', 'Środa', 'Wtorek', 'Poniedziałek', 'Wtorek', 'Piątek', 'Czwartek', 'Poniedziałek', 'Środa', 'Piątek', 'Wtorek', 'Środa']
    group_hours = ['11:45', '8:00', '8:00', '9:45', '13:30', '16:50', '13:30', '11:45', '15:10', '8:00', '8:00', '9:45']
    group_rooms = ['1.6.18', 'CW 8', '2.2.2', 'CW 9', '1.5.5', 'A6', '1.4.4', '2.2.2', '1.2.2', '2.2.2', '1.1.1', '4.4.4']

    teacher_editions = TeacherEdition.objects.all()
    teacher_editions_for_groups = [teacher_editions[1], teacher_editions[1], teacher_editions[1], teacher_editions[0], teacher_editions[0], teacher_editions[0], teacher_editions[2], teacher_editions[2], teacher_editions[2], teacher_editions[3], teacher_editions[3], teacher_editions[3]]
    
    
    students_all = Student.objects.all()

    print("Len teacher_editions: ", len(teacher_editions_for_groups))
    print("Len group_names: ", len(group_names))

    for i in range(len(group_names)):
        created_group = Group.objects.using(db_alias).create(
            name=group_names[i], day=group_days[i], hour=group_hours[i], room=group_rooms[i], teacherEdition=teacher_editions_for_groups[i]
        )
        for j in range(i * 8, i * 8 + 8):
            created_group.students.add(students_all[j])

    edition_servers = EditionServer.objects.all()

    for i in range(4, len(users_names)):
        if 4 <= i <= 27: # GRUPY 1-3
                DBAccount.objects.using(db_alias).create(
                    username=students_all[i-4].last_name + '-dbusername', password=students_all[i-4].last_name + '-dbpassword', additional_info="Additional info about dbaccount", is_moved=False, student=students_all[i-4], editionServer=edition_servers[1]
            )
        if 28 <= i <= 51: # GRUPY 4-6
                DBAccount.objects.using(db_alias).create(
                    username=students_all[i-4].last_name + '-dbusername', password=students_all[i-4].last_name + '-dbpassword', additional_info="Additional info about dbaccount", is_moved=False, student=students_all[i-4], editionServer=edition_servers[0]

            )
                DBAccount.objects.using(db_alias).create(
                    username=students_all[i-4].last_name + '-dbusername', password=students_all[i-4].last_name + '-dbpassword', additional_info="Additional info about dbaccount", is_moved=False, student=students_all[i-4], editionServer=edition_servers[4]
                    
            )
        if 52 <= i <= 75: # GRUPY 7-9
                DBAccount.objects.using(db_alias).create(
                    username=students_all[i-4].last_name + '-dbusername', password=students_all[i-4].last_name + '-dbpassword', additional_info="Additional info about dbaccount", is_moved=False, student=students_all[i-4], editionServer=edition_servers[2]
            )
        if 76 <= i <= 99: # GRUPY 10-12
                DBAccount.objects.using(db_alias).create(
                    username=students_all[i-4].last_name + '-dbusername', password=students_all[i-4].last_name + '-dbpassword', additional_info="Additional info about dbaccount", is_moved=False, student=students_all[i-4], editionServer=edition_servers[3]
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
                ('description', models.CharField(blank=True, default="", max_length=100)),
                ('active', models.BooleanField(default=False)),
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
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='editions', to='database.course')),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('description', models.CharField(blank=True, default="", max_length=100)),
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
                ('create_user_template', models.CharField(blank=True, default="", max_length=255)),
                ('modify_user_template', models.CharField(blank=True, default="", max_length=255)),
                ('delete_user_template', models.CharField(blank=True, default="", max_length=255)),
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
                ('additional_info', models.CharField(blank=True, default="", max_length=255)),
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
            field=models.CharField(blank=True, default="", max_length=100),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('day', models.CharField(blank=True, default="", max_length=30)),
                ('hour', models.CharField(blank=True, default="", max_length=30)),
                ('room', models.CharField(blank=True, default="", max_length=30)),
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
                ('description', models.CharField(blank=True, default="", max_length=100)),
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
                ('additional_info', models.CharField(blank=True, default="", max_length=255)),
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
                ('description', models.CharField(blank=True, default="", max_length=100)),
                ('permissions', models.ManyToManyField(blank=True, related_name='roles', to='database.permission')),
                ('users', models.ManyToManyField(blank=True, related_name='roles', to='database.user')),
            ],
        ),
        migrations.RunPython(forwards_func),
        migrations.AlterField(
            model_name='semester',
            name='year',
            field=models.CharField(max_length=9),
        ),
    ]
