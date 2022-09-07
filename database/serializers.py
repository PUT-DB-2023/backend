from rest_framework import serializers
from .models import User, Admin, Teacher, Student, Role, UserRole, Permission, RolePermission, Course, Semester, Edition, TeacherEdition, Group, Server, EditionServer, StudentGroup, DBAccount


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            'url',
            'first_name',
            'last_name',
            'email',
            'password',
        ]

class AdminSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Admin
        fields = [
            'url',
            'first_name',
            'last_name',
            'email',
            'password',
        ]

class TeacherSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Teacher
        fields = [
            'url',
            'first_name',
            'last_name',
            'email',
            'password',
        ]

class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        fields = [
            'url',
            'first_name',
            'last_name',
            'email',
            'password',
            'student_id',
        ]

class RoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Role
        fields = [
            'url',
            'name',
            'description',
        ]

class UserRoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserRole
        fields = [
            'url',
            'user',
            'role',
        ]

class PermissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Permission
        fields = [
            'url',
            'name',
            'description',
        ]

class RolePermissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RolePermission
        fields = [
            'url',
            'role',
            'permission',
        ]

class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = [
            'url',
            'name',
            'description',
        ]

class SemesterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Semester
        fields = [
            'url',
            'year',
            'winter',
        ]

class EditionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Edition
        fields = [
            'url',         
            'name',
            'description',
            'date_opened',
            'date_closed',
            'active',
            'semester',
            'course',
        ]

class TeacherEditionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TeacherEdition
        fields = [
            'url',
            'teacher',
            'edition',
        ]

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = [
            'url',
            'name',
            'day',
            'hour',
            'room',
            'teacherEdition',
        ]

class ServerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Server
        fields = [
            'url',
            'name',
            'ip',
            'port',
            'date_created',
            'active',
        ]

class EditionServerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EditionServer
        fields = [
            'url',
            'edition',
            'server',
            'additional_info',
        ]

class StudentGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StudentGroup
        fields = [
            'url',
            'student',
            'group',
        ]

class DBAccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DBAccount
        fields = [
            'url',
            'username',
            'password',
            'additional_info',
            'student',
            'editionServer',
        ]