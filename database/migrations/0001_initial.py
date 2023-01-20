# Generated by Django 4.0.5 on 2022-12-19 17:17

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
from django.contrib.auth.models import Permission as AuthPermission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model


import database.models
from database.password_generator import PasswordGenerator

import random


def forwards_func(apps, schema_editor):

    User = apps.get_model('database', 'User')
    Student = apps.get_model('database', 'Student')
    Teacher = apps.get_model('database', 'Teacher')
    DBAccount = apps.get_model('database', 'DBAccount')
    Group = apps.get_model('database', 'Group')
    TeacherEdition = apps.get_model('database', 'TeacherEdition')
    EditionServer = apps.get_model('database', 'EditionServer')
    Edition = apps.get_model('database', 'Edition')
    Semester = apps.get_model('database', 'Semester')
    Course = apps.get_model('database', 'Course')
    Dbms = apps.get_model('database', 'DBMS')
    Server = apps.get_model('database', 'Server')
    Major = apps.get_model('database', 'Major')
    AuthGroup = apps.get_model('auth.Group')

    teacher_group, _ = AuthGroup.objects.get_or_create(name='TeacherGroup')
    student_group, _ = AuthGroup.objects.get_or_create(name='StudentGroup')

    db_alias = schema_editor.connection.alias

    server_names = ['MySQL ZBD Server', 'Oracle ZBD Server', 'Postgres PBD Server', 'Mongo ZBDNS Server']
    server_ipss = ['185.180.207.251', '185.180.207.251', '185.180.207.251', 'mongo']
    server_ports = ['3306', '44475', '5432', '27017']
    server_date_createds = '2021-12-31'
    server_databases = ['mysql', 'xe', 'postgres', 'database']
    server_passwords = ['mysql12', 'oracle', 'postgres12', 'mongo12']
    dbms_names = ['MySQL', 'Oracle', 'PostgreSQL', 'MongoDB']
    server_users = ['root', 'system', 'postgres', 'root']
    server_create_user_templates = ["CREATE USER IF NOT EXISTS \"%s\"@'%%' IDENTIFIED BY '%s'", "CREATE USER \"%s\" IDENTIFIED BY \"%s\"", "CREATE USER \"%s\" WITH PASSWORD \'%s\';", 'readWrite']
    server_modify_user_templates = ["ALTER USER \"%s\" IDENTIFIED BY \'%s\';", "ALTER USER \"%s\" IDENTIFIED BY \"%s\"", "ALTER USER \"%s\" WITH PASSWORD \'%s\';", ""]
    server_delete_user_templates = ["DROP USER IF EXISTS \"%s\"@'%%';", "DROP USER \"%s\" CASCADE", "DROP USER IF EXISTS \"%s\";", ""]
    server_username_templates = [
        "INF_{NR_INDEKSU}", "{IMIE}_{NAZWISKO}", "{NAZWISKO}_{NR_INDEKSU}", "STUDENT_{NR_INDEKSU}", "INF_{NR_INDEKSU}"
    ]

    dbms = []

    Semester.objects.using(db_alias).create(
        start_year='2022',
        winter=False,
        active=True
    )

    for i in range(len(dbms_names)):
        dbms_object = Dbms.objects.using(db_alias).create(
            name=dbms_names[i]
        )
        dbms.append(dbms_object)

    for i in range(len(server_names)):
        Server.objects.using(db_alias).create(
            name=server_names[i],
            host=server_ipss[i],
            port=server_ports[i],
            date_created=server_date_createds,
            database=server_databases[i],
            password=server_passwords[i],
            dbms=dbms[i],
            user=server_users[i],
            create_user_template=server_create_user_templates[i],
            modify_user_template=server_modify_user_templates[i],
            delete_user_template=server_delete_user_templates[i],
            username_template=server_username_templates[i]
        )

    User.objects.create_superuser(first_name='Admin', last_name='Admin', email='admin@cs.put.poznan.pl', password='admin')

    add_course_permission, _ = AuthPermission.objects.get_or_create(codename='add_course', content_type=ContentType.objects.get_for_model(Course))
    change_course_permission, _ = AuthPermission.objects.get_or_create(codename='change_course', content_type=ContentType.objects.get_for_model(Course))
    view_course_permission, _ = AuthPermission.objects.get_or_create(codename='view_course', content_type=ContentType.objects.get_for_model(Course))
    delete_course_permission, _ = AuthPermission.objects.get_or_create(codename='delete_course', content_type=ContentType.objects.get_for_model(Course))

    add_edition_permission, _ = AuthPermission.objects.get_or_create(codename='add_edition', content_type=ContentType.objects.get_for_model(Edition))
    change_edition_permission, _ = AuthPermission.objects.get_or_create(codename='change_edition', content_type=ContentType.objects.get_for_model(Edition))
    view_edition_permission, _ = AuthPermission.objects.get_or_create(codename='view_edition', content_type=ContentType.objects.get_for_model(Edition))
    delete_edition_permission, _ = AuthPermission.objects.get_or_create(codename='delete_edition', content_type=ContentType.objects.get_for_model(Edition))

    add_user_permission, _ = AuthPermission.objects.get_or_create(codename='add_user', content_type=ContentType.objects.get_for_model(User))
    change_user_permission, _ = AuthPermission.objects.get_or_create(codename='change_user', content_type=ContentType.objects.get_for_model(User))
    view_user_permission, _ = AuthPermission.objects.get_or_create(codename='view_user', content_type=ContentType.objects.get_for_model(User))
    delete_user_permission, _ = AuthPermission.objects.get_or_create(codename='delete_user', content_type=ContentType.objects.get_for_model(User))
    reset_own_password_permission, _ = AuthPermission.objects.get_or_create(codename='reset_own_password', content_type=ContentType.objects.get_for_model(User))
    reset_student_password_permission, _ = AuthPermission.objects.get_or_create(codename='reset_student_password', content_type=ContentType.objects.get_for_model(User))
    update_password_after_reset_permission, _ = AuthPermission.objects.get_or_create(codename='update_password_after_reset', content_type=ContentType.objects.get_for_model(User))

    add_student_permission, _ = AuthPermission.objects.get_or_create(codename='add_student', content_type=ContentType.objects.get_for_model(Student))
    change_student_permission, _ = AuthPermission.objects.get_or_create(codename='change_student', content_type=ContentType.objects.get_for_model(Student))
    view_student_permission, _ = AuthPermission.objects.get_or_create(codename='view_student', content_type=ContentType.objects.get_for_model(Student))
    delete_student_permission, _ = AuthPermission.objects.get_or_create(codename='delete_student', content_type=ContentType.objects.get_for_model(Student))
    load_from_csv_permission, _ = AuthPermission.objects.get_or_create(codename='load_from_csv', content_type=ContentType.objects.get_for_model(Student))

    add_teacher_permission, _ = AuthPermission.objects.get_or_create(codename='add_teacher', content_type=ContentType.objects.get_for_model(Teacher))
    change_teacher_permission, _ = AuthPermission.objects.get_or_create(codename='change_teacher', content_type=ContentType.objects.get_for_model(Teacher))
    view_teacher_permission, _ = AuthPermission.objects.get_or_create(codename='view_teacher', content_type=ContentType.objects.get_for_model(Teacher))
    delete_teacher_permission, _ = AuthPermission.objects.get_or_create(codename='delete_teacher', content_type=ContentType.objects.get_for_model(Teacher))

    add_dbaccount_permission, _ = AuthPermission.objects.get_or_create(codename='add_dbaccount', content_type=ContentType.objects.get_for_model(DBAccount))
    change_dbaccount_permission, _ = AuthPermission.objects.get_or_create(codename='change_dbaccount', content_type=ContentType.objects.get_for_model(DBAccount))
    delete_dbaccount_permission, _ = AuthPermission.objects.get_or_create(codename='delete_dbaccount', content_type=ContentType.objects.get_for_model(DBAccount))
    view_dbaccount_permission, _ = AuthPermission.objects.get_or_create(codename='view_dbaccount', content_type=ContentType.objects.get_for_model(DBAccount))

    view_teacheredition_permission, _ = AuthPermission.objects.get_or_create(codename='view_teacheredition', content_type=ContentType.objects.get_for_model(TeacherEdition))

    change_active_semester_permission, _ = AuthPermission.objects.get_or_create(codename='change_active_semester', content_type=ContentType.objects.get_for_model(Semester))
    view_semester_permission, _ = AuthPermission.objects.get_or_create(codename='view_semester', content_type=ContentType.objects.get_for_model(Semester))

    remove_dbaccount_permission, _ = AuthPermission.objects.get_or_create(codename='move_dbaccount', content_type=ContentType.objects.get_for_model(DBAccount))
    reset_db_password_permission, _ = AuthPermission.objects.get_or_create(codename='reset_db_password', content_type=ContentType.objects.get_for_model(DBAccount))

    add_group_permission, _ = AuthPermission.objects.get_or_create(codename='add_group', content_type=ContentType.objects.get_for_model(Group))
    change_group_permission, _ = AuthPermission.objects.get_or_create(codename='change_group', content_type=ContentType.objects.get_for_model(Group))
    view_group_permission, _ = AuthPermission.objects.get_or_create(codename='view_group', content_type=ContentType.objects.get_for_model(Group))
    delete_group_permission, _ = AuthPermission.objects.get_or_create(codename='delete_group', content_type=ContentType.objects.get_for_model(Group))
    add_students_to_group_permission, _ = AuthPermission.objects.get_or_create(codename='add_students_to_group', content_type=ContentType.objects.get_for_model(Group))
    remove_student_from_group_permission, _ = AuthPermission.objects.get_or_create(codename='remove_student_from_group', content_type=ContentType.objects.get_for_model(Group))

    view_major_permission, _ = AuthPermission.objects.get_or_create(codename='view_major', content_type=ContentType.objects.get_for_model(Major))
    add_major_permission, _ = AuthPermission.objects.get_or_create(codename='add_major', content_type=ContentType.objects.get_for_model(Major))
    change_major_permission, _ = AuthPermission.objects.get_or_create(codename='change_major', content_type=ContentType.objects.get_for_model(Major))
    delete_major_permission, _ = AuthPermission.objects.get_or_create(codename='delete_major', content_type=ContentType.objects.get_for_model(Major))

    view_dbms_permission, _ = AuthPermission.objects.get_or_create(codename='view_dbms', content_type=ContentType.objects.get_for_model(Dbms))
    add_dbms_permission, _ = AuthPermission.objects.get_or_create(codename='add_dbms', content_type=ContentType.objects.get_for_model(Dbms))
    change_dbms_permission, _ = AuthPermission.objects.get_or_create(codename='change_dbms', content_type=ContentType.objects.get_for_model(Dbms))
    delete_dbms_permission, _ = AuthPermission.objects.get_or_create(codename='delete_dbms', content_type=ContentType.objects.get_for_model(Dbms))

    teacher_group.permissions.add(view_course_permission.pk)
    teacher_group.permissions.add(view_edition_permission.pk)
    teacher_group.permissions.add(add_group_permission.pk)
    teacher_group.permissions.add(change_group_permission.pk)
    teacher_group.permissions.add(delete_group_permission.pk)
    teacher_group.permissions.add(view_group_permission.pk)
    teacher_group.permissions.add(add_user_permission.pk)
    teacher_group.permissions.add(change_user_permission.pk)
    teacher_group.permissions.add(view_user_permission.pk)
    teacher_group.permissions.add(add_student_permission.pk)
    teacher_group.permissions.add(change_student_permission.pk)
    teacher_group.permissions.add(view_student_permission.pk)
    teacher_group.permissions.add(add_teacher_permission.pk)
    teacher_group.permissions.add(change_teacher_permission.pk)
    teacher_group.permissions.add(view_teacher_permission.pk)
    teacher_group.permissions.add(add_dbaccount_permission.pk)
    teacher_group.permissions.add(change_dbaccount_permission.pk)
    teacher_group.permissions.add(delete_dbaccount_permission.pk)
    teacher_group.permissions.add(view_dbaccount_permission.pk)
    teacher_group.permissions.add(remove_dbaccount_permission.pk)
    teacher_group.permissions.add(load_from_csv_permission.pk)
    teacher_group.permissions.add(view_teacheredition_permission.pk)
    teacher_group.permissions.add(add_students_to_group_permission.pk)
    teacher_group.permissions.add(remove_student_from_group_permission.pk)
    teacher_group.permissions.add(reset_own_password_permission.pk)
    teacher_group.permissions.add(reset_student_password_permission.pk)
    teacher_group.permissions.add(update_password_after_reset_permission.pk)
    teacher_group.permissions.add(view_major_permission.pk)
    teacher_group.permissions.add(reset_db_password_permission.pk)

    student_group.permissions.add(view_course_permission.pk)
    student_group.permissions.add(view_edition_permission.pk)
    student_group.permissions.add(view_group_permission.pk)
    student_group.permissions.add(view_student_permission.pk)
    student_group.permissions.add(view_teacher_permission.pk)
    student_group.permissions.add(view_user_permission.pk)
    student_group.permissions.add(view_dbaccount_permission.pk)
    student_group.permissions.add(view_major_permission.pk)
    student_group.permissions.add(reset_own_password_permission.pk)
    student_group.permissions.add(update_password_after_reset_permission.pk)
    student_group.permissions.add(reset_db_password_permission.pk)
        

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_student', models.BooleanField(default=False)),
                ('is_teacher', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', database.models.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('description', models.CharField(blank=True, default='', max_length=255)),
                ('active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='DBAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
                ('additional_info', models.CharField(blank=True, default='', max_length=255)),
                ('is_moved', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Edition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, default='', max_length=255)),
                ('date_opened', models.DateField(blank=True, null=True)),
                ('date_closed', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EditionServer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('additional_info', models.CharField(blank=True, default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('day', models.CharField(blank=True, default='', max_length=30)),
                ('hour', models.CharField(blank=True, default='', max_length=30)),
                ('room', models.CharField(blank=True, default='', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Major',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('description', models.CharField(blank=True, default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_year', models.IntegerField()),
                ('winter', models.BooleanField(default=True)),
                ('active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='teacher', to=settings.AUTH_USER_MODEL)),
            ],
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
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(max_length=6, unique=True)),
                ('major', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='students', to='database.major')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DBMS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.CharField(blank=True, default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('host', models.CharField(max_length=255)),
                ('port', models.CharField(max_length=255)),
                ('dbms', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.dbms', related_name='servers')),
                ('user', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('database', models.CharField(max_length=255)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('create_user_template', models.CharField(blank=True, default='', max_length=255)),
                ('modify_user_template', models.CharField(blank=True, default='', max_length=255)),
                ('delete_user_template', models.CharField(blank=True, default='', max_length=255)),
                ('custom_command_template', models.CharField(blank=True, default='', max_length=1023)),
                ('username_template', models.CharField(max_length=255, null=True)),
                ('editions', models.ManyToManyField(related_name='servers', through='database.EditionServer', to='database.edition')),
            ],
        ),
        migrations.AddConstraint(
            model_name='semester',
            constraint=models.UniqueConstraint(fields=('start_year', 'winter'), name='unique_semester'),
        ),
        migrations.AddConstraint(
            model_name='semester',
            constraint=models.CheckConstraint(check=models.Q(('start_year__gte', 2000), ('start_year__lte', 3000)), name='start_year_between_2020_and_3000'),
        ),
        migrations.AddField(
            model_name='group',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='groups', to='database.student'),
        ),
        migrations.AddField(
            model_name='group',
            name='teacherEdition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.teacheredition'),
        ),
        migrations.AddField(
            model_name='editionserver',
            name='edition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.edition'),
        ),
        migrations.AddField(
            model_name='editionserver',
            name='server',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.server'),
        ),
        migrations.AddField(
            model_name='edition',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='editions', to='database.course'),
        ),
        migrations.AddField(
            model_name='edition',
            name='semester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='editions', to='database.semester'),
        ),
        migrations.AddField(
            model_name='edition',
            name='teachers',
            field=models.ManyToManyField(blank=True, related_name='editions', through='database.TeacherEdition', to='database.teacher'),
        ),
        migrations.AddField(
            model_name='dbaccount',
            name='editionServer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='database.editionserver'),
        ),
        migrations.AddField(
            model_name='dbaccount',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='db_accounts', to='database.student'),
        ),
        migrations.AddField(
            model_name='course',
            name='major',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='courses', to='database.major'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
        migrations.AddConstraint(
            model_name='teacheredition',
            constraint=models.UniqueConstraint(fields=('teacher', 'edition'), name='unique_teacher_edition'),
        ),
        migrations.AddConstraint(
            model_name='edition',
            constraint=models.UniqueConstraint(fields=('course', 'semester'), name='unique_edition'),
        ),
        migrations.AddConstraint(
            model_name='dbaccount',
            constraint=models.UniqueConstraint(fields=('username', 'editionServer'), name='unique_username_editionserver'),
        ),
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='major',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AddConstraint(
            model_name='group',
            constraint=models.UniqueConstraint(fields=('teacherEdition', 'name'), name='unique_group'),
        ),
        migrations.AlterField(
            model_name='group',
            name='teacherEdition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='database.teacheredition'),
        ),
        migrations.RunPython(forwards_func),
    ]
