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


class Role(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)


class Permission(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)


class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)


class Course(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)


class Semester(models.Model):
    year = models.CharField(max_length=9)
    winter = models.BooleanField(default=True)


class Edition(models.Model):
    description = models.CharField(max_length=100)
    date_opened = models.DateField()
    date_closed = models.DateField()
    active = models.BooleanField(default=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class TeacherEdition(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE)


class Group(models.Model):
    name = models.CharField(max_length=30)
    day = models.CharField(max_length=30)
    hour = models.CharField(max_length=30)
    room = models.CharField(max_length=30, blank=True, default='')
    teacherEdition = models.ForeignKey(TeacherEdition, on_delete=models.CASCADE)


class Server(models.Model):
    name = models.CharField(max_length=30)
    ip = models.CharField(max_length=30)
    port = models.IntegerField()
    date_created = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)


class EditionServer(models.Model):
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE)
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    additional_info = models.CharField(max_length=100)


class StudentGroup(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)


class DBAccount(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    additional_info = models.CharField(max_length=100)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True)
    editionServer = models.ForeignKey(EditionServer, on_delete=models.SET_NULL, null=True, blank=True)
