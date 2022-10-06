from rest_framework import serializers
from .models import User, Admin, Teacher, Student, Role, Permission, Course, Semester, Edition, TeacherEdition, Group, Server, EditionServer, DBAccount


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
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
            'first_name',
            'last_name',
            'email',
            'password',
        ]

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = [
            'id',
            'name',
            'description',
        ]

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = [
            'id',
            'name',
            'description',
        ]

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'id',
            'name',
            'description',
        ]

class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = [
            'id',
            'year',
            'winter',
        ]

class EditionSerializer(serializers.ModelSerializer):
    teachers = TeacherSerializer(many=True, read_only=True)
    semester = SemesterSerializer(many=False, read_only=True)
    course = CourseSerializer(many=False, read_only=True)
    
    class Meta:
        model = Edition
        fields = [
            'id',
            'description',
            'date_opened',
            'date_closed',
            'active',
            'semester',
            'course',
            'teachers',
        ]

class TeacherEditionSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer(many=False, read_only=True)
    edition = EditionSerializer(many=False, read_only=True)

    class Meta:
        model = TeacherEdition
        fields = [
            'id',
            'teacher',
            'edition',
        ]


class StudentSerializer(serializers.ModelSerializer):
    # groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'password',
            'student_id',
            # 'groups',
        ]


class TeacherEditionSerializerForGroup(serializers.ModelSerializer):
    teacher = TeacherSerializer(many=False, read_only=True)

    class Meta:
        model = TeacherEdition
        fields = [
            'id',
            'teacher',
            'edition',
        ]


class GroupSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True, read_only=True)
    # edition = EditionSerializer(many=False, read_only=True)
    # teacherEdition = TeacherEditionSerializer(many=False, read_only=True)
    teacherEdition = TeacherEditionSerializerForGroup(many=False, read_only=True)

    class Meta:
        model = Group
        fields = [
            'id',
            'name',
            'day',
            'hour',
            'room',
            'teacherEdition',
            # 'teacher',
            # 'edition',
            'students',
        ]





class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = [
            'id',
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
            'edition',
            'server',
            'additional_info',
        ]

class DBAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = DBAccount
        fields = [
            'id',
            'username',
            'password',
            'additional_info',
            'student',
            'editionServer',
            'isMovedToExtDB'
        ]