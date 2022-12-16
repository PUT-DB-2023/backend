from email.policy import default
from enum import unique
from polymorphic.models import PolymorphicModel
from django.db import models
from django.db.models import CheckConstraint, Q, F
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher')


class Student(models.Model):
    student_id = models.CharField(max_length=6, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    major = models.ForeignKey('Major', on_delete=models.SET_NULL, blank=True, null=True, related_name='students')


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
        print(f"Saving course {self.name}")
        # check if self.editions.all() is empty
        if self.editions.all():
            print(f"Editions: {self.editions.all()}")
            for edition in self.editions.all():
                if edition.semester.active:
                    print(f"Found an active semester: {edition.semester}")
                    self.active = True
                    break
                else:
                    print(f"Found an inactive semester: {edition.semester}")
                    self.active = False
        else:
            print(f"No editions found for course: {self}")
            self.active = False
        super().save(*args, **kwargs)


class Semester(models.Model):
    start_year = models.IntegerField()
    winter = models.BooleanField(default=True)
    active = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['start_year', 'winter'], name='unique_semester'),
            models.CheckConstraint(check=Q(start_year__gte=2000) & Q(start_year__lte=3000), name='start_year_between_2020_and_3000'),
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for course in Course.objects.all():
            print(f"Checking course: {course}")
            course.save()
    
    # override update method to check if it can be activated
    # def update(self, *args, **kwargs):
    #     print(f"Updating semester: {self}, {self.active}")
    #     if Semester.objects.filter(active=True).count() == 0:
    #         print(f"No active semester found, activating semester: {self}")
    #         self.active = True

    #     super().update(*args, **kwargs)
    
    # override delete method to disallow deletion of an active semester
    def delete(self, *args, **kwargs):
        print("self.active: ", self.active)
        if self.active:
            print(f"Cannot delete active semester: {self}")
            raise Exception("Cannot delete an active semester")
        else:
            print(f"Deleting semester: {self}")
            super().delete(*args, **kwargs)
        for course in Course.objects.all():
            print(f"Checking course: {course}")
            course.save()

class Edition(models.Model):
    description = models.CharField(max_length=255, blank=True, default='')
    date_opened = models.DateField(blank=True, null=True)
    date_closed = models.DateField(blank=True, null=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='editions')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='editions')
    teachers = models.ManyToManyField(Teacher, through='TeacherEdition', blank=True, related_name='editions')
    # servers = models.ManyToManyField('Server', through='EditionServer', blank=True, related_name='editions')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['course', 'semester'], name='unique_edition'),
        ]

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

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['teacher', 'edition'], name='unique_teacher_edition'),
        ]


class Group(models.Model):
    name = models.CharField(max_length=30)
    day = models.CharField(max_length=30, blank=True, default='')
    hour = models.CharField(max_length=30, blank=True, default='')
    room = models.CharField(max_length=30, blank=True, default='')
    teacherEdition = models.ForeignKey(TeacherEdition, on_delete=models.CASCADE)
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
    editions = models.ManyToManyField(Edition, through='EditionServer', related_name='servers')
    create_user_template = models.CharField(max_length=255, blank=True, default='')
    modify_user_template = models.CharField(max_length=255, blank=True, default='')
    delete_user_template = models.CharField(max_length=255, blank=True, default='')
    username_template = models.CharField(max_length=255, null=True)

class EditionServer(models.Model):
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE)
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    additional_info = models.CharField(max_length=255, blank=True, default='')
    # username_template = models.CharField(max_length=255, null=True)
    # passwd_template = models.CharField(max_length=255, null=True)

class DBAccount(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    additional_info = models.CharField(max_length=255, blank=True, default='')
    is_moved = models.BooleanField(default=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, related_name='db_accounts')
    editionServer = models.ForeignKey(EditionServer, on_delete=models.SET_NULL, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['username', 'editionServer'], name='unique_username_editionserver'),
        ]
