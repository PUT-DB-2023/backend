from email.policy import default
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


class Permission(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100, blank=True, default='')


class Role(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100, blank=True, default='')
    permisssions = models.ManyToManyField(Permission, related_name='roles', blank=True)
    users = models.ManyToManyField(User, related_name='roles', blank=True)


class Major(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100, blank=True, default='')

class Course(models.Model):
    name = models.CharField(max_length=30, unique=True)
    major = models.ForeignKey(Major, on_delete=models.SET_NULL, blank=True, null=True, related_name='courses')
    description = models.CharField(max_length=100, blank=True, default='')


class Semester(models.Model):
    year = models.CharField(max_length=9)
    winter = models.BooleanField(default=True)


class Edition(models.Model):
    description = models.CharField(max_length=100, blank=True, default='')
    date_opened = models.DateField(blank=True, null=True)
    date_closed = models.DateField(blank=True, null=True)
    active = models.BooleanField(default=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teachers = models.ManyToManyField(Teacher, through='TeacherEdition', related_name='editions', blank=True)


class TeacherEdition(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE)


class Group(models.Model):
    name = models.CharField(max_length=30)
    day = models.CharField(max_length=30, blank=True, default='')
    hour = models.CharField(max_length=30, blank=True, default='')
    room = models.CharField(max_length=30, blank=True, default='')
    teacherEdition = models.ForeignKey(TeacherEdition, on_delete=models.SET_NULL, default=None, null=True)
    students = models.ManyToManyField(Student, related_name='groups')


class Server(models.Model):
    name = models.CharField(max_length=30)
    ip = models.CharField(max_length=30)
    port = models.CharField(max_length=10)
    provider = models.CharField(max_length=30)
    user = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    database = models.CharField(max_length=30)
    date_created = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)
    edition = models.ManyToManyField(Edition, through='EditionServer', related_name='servers')


class EditionServer(models.Model):
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE)
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    additional_info = models.CharField(max_length=255, blank=True, default='')
    username_template = models.CharField(max_length=255, null=True)
    passwd_template = models.CharField(max_length=255, null=True)

class DBAccount(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    additional_info = models.CharField(max_length=255, blank=True, default='')
    isMovedToExtDB = models.BooleanField(default=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, related_name='db_accounts')
    editionServer = models.ForeignKey(EditionServer, on_delete=models.SET_NULL, null=True)
