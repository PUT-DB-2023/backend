from rest_framework import serializers
from .models import User, Admin, Teacher, Student, Role, UserRole, Permission, RolePermission, Course, Semester, Edition, TeacherEdition, Group, Server, EditionServer, StudentGroup, DBAccount


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            # 'url',
            'first_name',
            'last_name',
            'email',
            'password',
        ]

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = [
            'id',
            # 'url',
            'first_name',
            'last_name',
            'email',
            'password',
        ]

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = [
            'id',
            # 'url',
            'first_name',
            'last_name',
            'email',
            'password',
        ]

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'id',
            # 'url',
            'first_name',
            'last_name',
            'email',
            'password',
            'student_id',
        ]

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = [
            'id',
            # 'url',
            'name',
            'description',
        ]

class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = [
            'id',
            # 'url',
            'user',
            'role',
        ]

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = [
            'id',
            # 'url',
            'name',
            'description',
        ]

class RolePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePermission
        fields = [
            'id',
            # 'url',
            'role',
            'permission',
        ]

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'id',
            # 'url',
            'name',
            'description',
        ]

class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = [
            'id',
            # 'url',
            'year',
            'winter',
        ]

class EditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edition
        fields = [
            'id',
            # 'url',
            'name',
            'description',
            'date_opened',
            'date_closed',
            'active',
            'semester',
            'course',
        ]

class TeacherEditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherEdition
        fields = [
            'id',
            # 'url',
            'teacher',
            'edition',
        ]

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = [
            'id',
            # 'url',
            'name',
            'day',
            'hour',
            'room',
            'teacherEdition',
        ]

class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = [
            'id',
            # 'url',
            'name',
            'ip',
            'port',
            'date_created',
            'active',
        ]

class EditionServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = EditionServer
        fields = [
            'id',
            # 'url',
            'edition',
            'server',
            'additional_info',
        ]

class StudentGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentGroup
        fields = [
            'id',
            # 'url',
            'student',
            'group',
        ]

class DBAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = DBAccount
        fields = [
            'id',
            # 'url',
            'username',
            'password',
            'additional_info',
            'student',
            'editionServer',
        ]