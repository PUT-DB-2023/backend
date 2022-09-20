from rest_framework import serializers
from .models import User, Admin, Teacher, Student, Role, UserRole, Permission, RolePermission, Course, Semester, Edition, TeacherEdition, Group, Server, EditionServer, StudentGroup, DBAccount


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
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
            'id',
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
            'id',
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
            'id',
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
            'id',
            'url',
            'name',
            'description',
        ]

class UserRoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserRole
        fields = [
            'id',
            'url',
            'user',
            'role',
        ]

class PermissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Permission
        fields = [
            'id',
            'url',
            'name',
            'description',
        ]

class RolePermissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RolePermission
        fields = [
            'id',
            'url',
            'role',
            'permission',
        ]

class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = [
            'id',
            'url',
            'name',
            'description',
        ]

class SemesterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Semester
        fields = [
            'id',
            'url',
            'year',
            'winter',
        ]

class EditionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Edition
        fields = [
            'id',
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
            'id',
            'url',
            'teacher',
            'edition',
        ]

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = [
            'id',
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
            'id',
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
            'id',
            'url',
            'edition',
            'server',
            'additional_info',
        ]

class StudentGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StudentGroup
        fields = [
            'id',
            'url',
            'student',
            'group',
        ]

class DBAccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DBAccount
        fields = [
            'id',
            'url',
            'username',
            'password',
            'additional_info',
            'student',
            'editionServer',
        ]