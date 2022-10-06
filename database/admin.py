from django.contrib import admin
from .models import User, Admin, Teacher, Student, Role, Permission, Course, Semester, Edition, TeacherEdition, Group, Server, EditionServer, DBAccount

# Register your models here.
admin.site.register(User)
admin.site.register(Admin)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Role)
admin.site.register(Permission)
admin.site.register(Course)
admin.site.register(Semester)
admin.site.register(Edition)
admin.site.register(TeacherEdition)
admin.site.register(Group)
admin.site.register(Server)
admin.site.register(EditionServer)
admin.site.register(DBAccount)
