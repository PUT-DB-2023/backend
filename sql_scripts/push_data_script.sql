INSERT INTO database_server
(id, "name", ip, port, date_created, active)
VALUES(1, 'POSTGRES', '150.24.150.30', 5432, '2017-08-09', true);
INSERT INTO database_server
(id, "name", ip, port, date_created, active)
VALUES(2, 'MYSQL', '170.225.225.225', 1234, '2015-04-06', false);


INSERT INTO database_course
(id, "name", description)
VALUES(1, 'ZARZADZANIE BAZAMI DANYCH', 'Kurs zarządzania bazami danych SQL i noSQL');
INSERT INTO database_course
(id, "name", description)
VALUES(2, 'BAZY DANYCH', 'Kurs podstaw baz danych');


INSERT INTO database_semester
(id, "year", winter)
VALUES(1, 3, true);
INSERT INTO database_semester
(id, "year", winter)
VALUES(2, 2, false);
INSERT INTO database_semester
(id, "year", winter)
VALUES(3, 1, true);



INSERT INTO database_user
(id, first_name, last_name, email, "password", polymorphic_ctype_id)
VALUES(2, 'Jakub', 'Wrobel', 'jakub.p.wrobel@student.put.poznan.pl', 'haslojakuba', 15);
INSERT INTO database_user
(id, first_name, last_name, email, "password", polymorphic_ctype_id)
VALUES(3, 'Krystian', 'Jakusik', 'krystian.jakusik@student.put.poznan.pl', 'krystian123', 15);
INSERT INTO database_user
(id, first_name, last_name, email, "password", polymorphic_ctype_id)
VALUES(4, 'Przemysław', 'Woźniak', 'przemyslaw.wozniak@student.put.poznan.pl', 'przemekwprzemek', 15);
INSERT INTO database_user
(id, first_name, last_name, email, "password", polymorphic_ctype_id)
VALUES(5, 'Bartosz', 'Bębel', 'bartosz.bebel@cs.put.poznan.pl', 'Bartosz', 14);
INSERT INTO database_user
(id, first_name, last_name, email, "password", polymorphic_ctype_id)
VALUES(6, 'Michał', 'Apolinarski', 'michal.apolinarski@cs.put.poznan.pl', 'michalapol123', 16);


INSERT INTO database_admin
(user_ptr_id)
VALUES(5);


INSERT INTO database_student
(user_ptr_id, student_id)
VALUES(2, '145188');
INSERT INTO database_student
(user_ptr_id, student_id)
VALUES(3, '145318');
INSERT INTO database_student
(user_ptr_id, student_id)
VALUES(4, '145423');

INSERT INTO database_teacher
(user_ptr_id)
VALUES(6);



INSERT INTO database_edition
(id, "name", description, date_opened, date_closed, active, course_id, semester_id)
VALUES(1, '2019/2020', '-', '2019-01-09', '2020-01-03', false, 1, 2);
INSERT INTO database_edition
(id, "name", description, date_opened, date_closed, active, course_id, semester_id)
VALUES(2, '2022/2023', '-', '2022-01-10', '2023-01-03', true, 2, 3);


INSERT INTO database_editionserver
(id, additional_info, edition_id, server_id)
VALUES(1, 'Additional info about server 1', 1, 1);
INSERT INTO database_editionserver
(id, additional_info, edition_id, server_id)
VALUES(2, 'Additional info about server 2', 2, 2);


INSERT INTO database_teacheredition
(id, edition_id, teacher_id)
VALUES(1, 1, 6);
INSERT INTO database_teacheredition
(id, edition_id, teacher_id)
VALUES(2, 2, 6);


INSERT INTO database_group
(id, "name", "day", "hour", room, "teacherEdition_id")
VALUES(1, 'L10', 'Monday', '11:45', '3a', 1);
INSERT INTO database_group
(id, "name", "day", "hour", room, "teacherEdition_id")
VALUES(2, 'L5', 'Tuesday', '13:30', '11b', 2);


INSERT INTO database_studentgroup
(id, group_id, student_id)
VALUES(1, 1, 3);
INSERT INTO database_studentgroup
(id, group_id, student_id)
VALUES(2, 2, 4);
INSERT INTO database_studentgroup
(id, group_id, student_id)
VALUES(3, 1, 2);


INSERT INTO database_dbaccount
(id, username, "password", additional_info, "editionServer_id", student_id)
VALUES(1, 'jwrobel', 'inf145188', 'Additional info about user id 1', 1, 2);
INSERT INTO database_dbaccount
(id, username, "password", additional_info, "editionServer_id", student_id)
VALUES(2, 'pwozniak', 'inf145423', 'Additional info about user id 2', 2, 3);
INSERT INTO database_dbaccount
(id, username, "password", additional_info, "editionServer_id", student_id)
VALUES(3, 'kjakusik', 'inf145318', 'Additional info about user id 3', 1, 4);






