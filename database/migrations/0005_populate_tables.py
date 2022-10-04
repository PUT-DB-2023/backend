from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0004_alter_edition_date_closed_alter_edition_date_opened'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                delete from database_dbaccount;
                delete from database_studentgroup;
                delete from database_group;
                delete from database_teacheredition;
                delete from database_editionserver;
                delete from database_edition;
                delete from database_teacher;
                delete from database_student;
                delete from database_admin;
                delete from database_user;
                delete from database_semester;
                delete from database_course;
                delete from database_server;

                INSERT INTO public.database_server
                (id, "name", ip, port, date_created, active)
                VALUES(1, 'POSTGRES', '150.24.150.30', 5432, '2017-08-09', true);
                INSERT INTO public.database_server
                (id, "name", ip, port, date_created, active)
                VALUES(2, 'MYSQL', '170.225.225.225', 1234, '2015-04-06', true);
                INSERT INTO public.database_server
                (id, "name", ip, port, date_created, active)
                VALUES(3, 'MONGO_DB', '155.155.200.205', 3333, '2019-05-11', false);
                INSERT INTO public.database_server
                (id, "name", ip, port, date_created, active)
                VALUES(4, 'CASSANDRA', '120.120.255.255', 1234, '2016-01-04', true);
                INSERT INTO public.database_server
                (id, "name", ip, port, date_created, active)
                VALUES(5, 'ORACLE', '111.111.120.125', 1111, '2022-12-12', false);
                INSERT INTO public.database_server
                (id, "name", ip, port, date_created, active)
                VALUES(6, 'ORACLE_NEW', '111.111.120.145', 2537, '2023-05-08', true);



                INSERT INTO public.database_course
                (id, "name", description)
                VALUES(1, 'Zarządzanie bazami danych', 'Kurs zarządzania bazami danych SQL i noSQL');
                INSERT INTO public.database_course
                (id, "name", description)
                VALUES(2, 'Podstawy baz danych', 'Kurs podstaw baz danych');
                INSERT INTO public.database_course
                (id, "name", description)
                VALUES(3, 'Administacja baz danych', 'Kurs administrowania baz danych');
                INSERT INTO public.database_course
                (id, "name", description)
                VALUES(4, 'Projektowanie baz danych', 'Kurs projektowania baz danych');
                INSERT INTO public.database_course
                (id, "name", description)
                VALUES(5, 'Zaawansowane bazy danych', 'Kurs zaawansowany baz danych');


                INSERT INTO public.database_semester
                (id, "year", winter)
                VALUES(1, '2020/2021', true);
                INSERT INTO public.database_semester
                (id, "year", winter)
                VALUES(2, '2017/2018', false);
                INSERT INTO public.database_semester
                (id, "year", winter)
                VALUES(3, '2019/2020', true);
                INSERT INTO public.database_semester
                (id, "year", winter)
                VALUES(4, '2019/2020', false);
                INSERT INTO public.database_semester
                (id, "year", winter)
                VALUES(5, '2022/2023', true);



                INSERT INTO public.database_user
                (id, first_name, last_name, email, "password", polymorphic_ctype_id)
                VALUES(2, 'Jakub', 'Wrobel', 'jakub.p.wrobel@student.put.poznan.pl', 'haslojakuba', 15);
                INSERT INTO public.database_user
                (id, first_name, last_name, email, "password", polymorphic_ctype_id)
                VALUES(3, 'Krystian', 'Jakusik', 'krystian.jakusik@student.put.poznan.pl', 'krystian123', 15);
                INSERT INTO public.database_user
                (id, first_name, last_name, email, "password", polymorphic_ctype_id)
                VALUES(4, 'Przemysław', 'Woźniak', 'przemyslaw.wozniak@student.put.poznan.pl', 'przemekwprzemek', 15);
                INSERT INTO public.database_user
                (id, first_name, last_name, email, "password", polymorphic_ctype_id)
                VALUES(5, 'Bartosz', 'Bębel', 'bartosz.bebel@cs.put.poznan.pl', 'Bartosz', 14);
                INSERT INTO public.database_user
                (id, first_name, last_name, email, "password", polymorphic_ctype_id)
                VALUES(6, 'Michał', 'Apolinarski', 'michal.apolinarski@cs.put.poznan.pl', 'michalapol123', 16);
                INSERT INTO public.database_user
                (id, first_name, last_name, email, "password", polymorphic_ctype_id)
                VALUES(7, 'Jan', 'Kowalski', 'jan.kowalski@student.put.poznan.pl', 'jkowal', 15);
                INSERT INTO public.database_user
                (id, first_name, last_name, email, "password", polymorphic_ctype_id)
                VALUES(8, 'Michał', 'Nowak', 'michal.t.nowak@student.put.poznan.pl', 'nowakkk', 15);
                INSERT INTO public.database_user
                (id, first_name, last_name, email, "password", polymorphic_ctype_id)
                VALUES(9, 'Arkadiusz', 'Instruktor', 'arkadiusz.instruktor@cs.put.poznan.pl', 'arekins', 14);
                INSERT INTO public.database_user
                (id, first_name, last_name, email, "password", polymorphic_ctype_id)
                VALUES(10, 'Tomasz', 'Nauczycielski', 'tomasz.nauczycielski@cs.put.poznan.pl', 'tomnau', 16);
                INSERT INTO public.database_user
                (id, first_name, last_name, email, "password", polymorphic_ctype_id)
                VALUES(11, 'Wiktor', 'Wykładnik', 'wiktor.wykładnik@cs.put.poznan.pl', 'potega123', 16);
                INSERT INTO public.database_user
                (id, first_name, last_name, email, "password", polymorphic_ctype_id)
                VALUES(12, 'Konrad', 'Indeksowy', 'konrad.indeksowy@cs.put.poznan.pl', 'indeksik213', 16);



                INSERT INTO public.database_admin
                (user_ptr_id)
                VALUES(5);
                INSERT INTO public.database_admin
                (user_ptr_id)
                VALUES(9);


                INSERT INTO public.database_student
                (user_ptr_id, student_id)
                VALUES(2, '145188');
                INSERT INTO public.database_student
                (user_ptr_id, student_id)
                VALUES(3, '145318');
                INSERT INTO public.database_student
                (user_ptr_id, student_id)
                VALUES(4, '145423');
                INSERT INTO public.database_student
                (user_ptr_id, student_id)
                VALUES(7, '145222');
                INSERT INTO public.database_student
                (user_ptr_id, student_id)
                VALUES(8, '145111');


                INSERT INTO public.database_teacher
                (user_ptr_id)
                VALUES(6);
                INSERT INTO public.database_teacher
                (user_ptr_id)
                VALUES(10);
                INSERT INTO public.database_teacher
                (user_ptr_id)
                VALUES(11);
                INSERT INTO public.database_teacher
                (user_ptr_id)
                VALUES(12);



                INSERT INTO public.database_edition
                (id, description, date_opened, date_closed, active, course_id, semester_id)
                VALUES(1, '-', '2019-01-09', '2020-01-03', false, 1, 2);
                INSERT INTO public.database_edition
                (id, description, date_opened, date_closed, active, course_id, semester_id)
                VALUES(2, '-', '2022-01-10', '2023-01-03', true, 2, 3);
                INSERT INTO public.database_edition
                (id, description, date_opened, date_closed, active, course_id, semester_id)
                VALUES(3, '-', '2023-01-08', '2023-01-01', true, 3, 3);
                INSERT INTO public.database_edition
                (id, description, date_opened, date_closed, active, course_id, semester_id)
                VALUES(4, '-', '2012-01-01', '2016-01-01', false, 4, 4);



                INSERT INTO public.database_editionserver
                (id, additional_info, edition_id, server_id)
                VALUES(1, 'Additional info about server 1', 1, 1);
                INSERT INTO public.database_editionserver
                (id, additional_info, edition_id, server_id)
                VALUES(2, 'Additional info about server 2', 2, 2);
                INSERT INTO public.database_editionserver
                (id, additional_info, edition_id, server_id)
                VALUES(3, 'Additional info about server 3', 4, 1);
                INSERT INTO public.database_editionserver
                (id, additional_info, edition_id, server_id)
                VALUES(4, 'Additional info about server 4', 3, 2);



                INSERT INTO public.database_teacheredition
                (id, edition_id, teacher_id)
                VALUES(1, 1, 6);
                INSERT INTO public.database_teacheredition
                (id, edition_id, teacher_id)
                VALUES(2, 2, 6);
                INSERT INTO public.database_teacheredition
                (id, edition_id, teacher_id)
                VALUES(3, 2, 10);
                INSERT INTO public.database_teacheredition
                (id, edition_id, teacher_id)
                VALUES(4, 3, 10);
                INSERT INTO public.database_teacheredition
                (id, edition_id, teacher_id)
                VALUES(5, 3, 11);
                INSERT INTO public.database_teacheredition
                (id, edition_id, teacher_id)
                VALUES(6, 4, 12);



                INSERT INTO public.database_group
                (id, "name", "day", "hour", room, "teacherEdition_id")
                VALUES(1, 'L10', 'Monday', '11:45', '3a', 1);
                INSERT INTO public.database_group
                (id, "name", "day", "hour", room, "teacherEdition_id")
                VALUES(2, 'L5', 'Tuesday', '13:30', '11b', 2);
                INSERT INTO public.database_group
                (id, "name", "day", "hour", room, "teacherEdition_id")
                VALUES(3, 'L1', 'Friday', '10:00', '1', 3);
                INSERT INTO public.database_group
                (id, "name", "day", "hour", room, "teacherEdition_id")
                VALUES(4, 'L2', 'Thursday', '12:00', '2', 4);
                INSERT INTO public.database_group
                (id, "name", "day", "hour", room, "teacherEdition_id")
                VALUES(5, 'L3', 'Wednesday', '11:00', '3', 5);
                INSERT INTO public.database_group
                (id, "name", "day", "hour", room, "teacherEdition_id")
                VALUES(6, 'L4', 'Monday', '10:00', '4', 6);



                INSERT INTO public.database_studentgroup
                (id, group_id, student_id)
                VALUES(1, 1, 3);
                INSERT INTO public.database_studentgroup
                (id, group_id, student_id)
                VALUES(2, 2, 4);
                INSERT INTO public.database_studentgroup
                (id, group_id, student_id)
                VALUES(3, 1, 2);
                INSERT INTO public.database_studentgroup
                (id, group_id, student_id)
                VALUES(4, 3, 7);
                INSERT INTO public.database_studentgroup
                (id, group_id, student_id)
                VALUES(5, 4, 8);



                INSERT INTO public.database_dbaccount
                (id, username, "password", additional_info, "editionServer_id", student_id)
                VALUES(1, 'jwrobel', 'inf145188', 'Additional info about user id 1', 1, 2);
                INSERT INTO public.database_dbaccount
                (id, username, "password", additional_info, "editionServer_id", student_id)
                VALUES(2, 'pwozniak', 'inf145423', 'Additional info about user id 2', 2, 3);
                INSERT INTO public.database_dbaccount
                (id, username, "password", additional_info, "editionServer_id", student_id)
                VALUES(3, 'kjakusik', 'inf145318', 'Additional info about user id 3', 1, 4);
                INSERT INTO public.database_dbaccount
                (id, username, "password", additional_info, "editionServer_id", student_id)
                VALUES(4, 'jkowal', 'inf145111', 'Additional info about user id 4', 3, 7);
                INSERT INTO public.database_dbaccount
                (id, username, "password", additional_info, "editionServer_id", student_id)
                VALUES(5, 'mnowak', 'inf145222', 'Additional info about user id 5', 4, 8);
                """)]