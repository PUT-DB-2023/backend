from django.contrib import admin
from .models import User, Teacher, Student, Course, Semester, Edition, TeacherEdition, Group, Server, EditionServer, DBAccount, Major, DBMS
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(User)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Semester)
admin.site.register(Edition)
admin.site.register(TeacherEdition)
admin.site.register(Group)
admin.site.register(Server)
admin.site.register(EditionServer)
admin.site.register(DBAccount)
admin.site.register(Major)
admin.site.register(DBMS)