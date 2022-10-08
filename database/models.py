from enum import unique
from polymorphic.models import PolymorphicModel
from django.db import models


class User(PolymorphicModel):
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=30)


class Admin(User):
    pass


class Teacher(User):
    pass


class Student(User):
    student_id = models.CharField(max_length=6, unique=True)
    # groups = models.ManyToManyField(Group, related_name='groups', blank=True, null=True)


class Permission(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)


class Role(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)
    permisssions = models.ManyToManyField(Permission)
    users = models.ManyToManyField(User)


class Course(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)


class Semester(models.Model):
    year = models.CharField(max_length=9)
    winter = models.BooleanField(default=True)


class Edition(models.Model):
    description = models.CharField(max_length=100)
    date_opened = models.DateField(blank=True, null=True)
    date_closed = models.DateField(blank=True, null=True)
    active = models.BooleanField(default=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teachers = models.ManyToManyField(Teacher, through='TeacherEdition')


class TeacherEdition(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE)


class Group(models.Model):
    name = models.CharField(max_length=30)
    day = models.CharField(max_length=30)
    hour = models.CharField(max_length=30)
    room = models.CharField(max_length=30, blank=True, default='')
    teacherEdition = models.ForeignKey(TeacherEdition, on_delete=models.SET_NULL, default=None, null=True)
    students = models.ManyToManyField(Student, related_name='groups')


class Server(models.Model):
    name = models.CharField(max_length=30)
    ip = models.CharField(max_length=30)
    port = models.CharField(max_length=10)
    date_created = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)
    edition = models.ManyToManyField(Edition, through='EditionServer')


class EditionServer(models.Model):
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE)
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    additional_info = models.CharField(max_length=255, blank=True, default='')


class DBAccount(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    additional_info = models.CharField(max_length=255)
    isMovedToExtDB = models.BooleanField(default=False)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    editionServer = models.ForeignKey(EditionServer, on_delete=models.SET_NULL, null=True)
