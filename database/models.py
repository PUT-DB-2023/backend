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
    description = models.CharField(max_length=255, blank=True, default='')


class Role(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=255, blank=True, default='')
    permissions = models.ManyToManyField(Permission, blank=True, related_name='roles')
    users = models.ManyToManyField(User, related_name='roles', blank=True)


class Major(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=255, blank=True, default='')

class Course(models.Model):
    name = models.CharField(max_length=30, unique=True)
    major = models.ForeignKey(Major, on_delete=models.SET_NULL, blank=True, null=True, related_name='courses')
    description = models.CharField(max_length=255, blank=True, default='')
    active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # check if self.editions.all() is empty
        if self.editions.all():
            print(f"Editions: {self.editions.all()}")
            for edition in self.editions.all():
                if edition.semester.active:
                    print(f"Found active semester: {edition.semester}")
                    self.active = True
                    break
                else:
                    print(f"Found inactive semester: {edition.semester}")
                    self.active = False
        else:
            print(f"No editions found for course: {self}")
            self.active = False
        super().save(*args, **kwargs)


class Semester(models.Model):
    year = models.CharField(max_length=9)
    winter = models.BooleanField(default=True)
    active = models.BooleanField(default=False)


class Edition(models.Model):
    description = models.CharField(max_length=255, blank=True, default='')
    date_opened = models.DateField(blank=True, null=True)
    date_closed = models.DateField(blank=True, null=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='editions')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='editions')
    teachers = models.ManyToManyField(Teacher, through='TeacherEdition', blank=True, related_name='editions')

    def save(self, *args, **kwargs):
        print(f"Course: {self.course}, Course active: {self.course.active}, semester active: {self.semester.active}")
        super().save(*args, **kwargs)
        self.course.save()

    # override create method to check if the course is active
    def create(self, *args, **kwargs):
        super().create(*args, **kwargs)
        self.course.save()

    # override delete method to check if the course is active
    def delete(self, *args, **kwargs):
        print(f"Deleting edition: {self}")
        super().delete(*args, **kwargs)
        print("Saving course")
        self.course.save()


class TeacherEdition(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE)


class Group(models.Model):
    name = models.CharField(max_length=30)
    day = models.CharField(max_length=30, blank=True, default='')
    hour = models.CharField(max_length=30, blank=True, default='')
    room = models.CharField(max_length=30, blank=True, default='')
    teacherEdition = models.ForeignKey(TeacherEdition, on_delete=models.SET_NULL, default=None, null=True)
    students = models.ManyToManyField(Student, blank=True, related_name='groups')


# class DBProvider(models.Model):
#     name = models.CharField(max_length=30)
#     description = models.CharField(max_length=255, blank=True, default='')

class Server(models.Model):
    name = models.CharField(max_length=30)
    ip = models.CharField(max_length=30)
    port = models.CharField(max_length=10)
    provider = models.CharField(max_length=30)
    # provider = models.ForeignKey(DBProvider, on_delete=models.SET_NULL, null=True, related_name='servers')
    user = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    database = models.CharField(max_length=30)
    date_created = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)
    edition = models.ManyToManyField(Edition, through='EditionServer', related_name='servers')
    create_user_template = models.CharField(max_length=255, blank=True, default='')
    modify_user_template = models.CharField(max_length=255, blank=True, default='')
    delete_user_template = models.CharField(max_length=255, blank=True, default='')

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
    is_moved = models.BooleanField(default=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, related_name='db_accounts')
    editionServer = models.ForeignKey(EditionServer, on_delete=models.SET_NULL, null=True)
