from rest_framework.serializers import ModelSerializer
# from rest_framework_serializer_extensions.serializers import SerializerExtensionsMixin
from .models import User, Admin, Teacher, Student, Role, Permission, Course, Semester, Edition, TeacherEdition, Group, Server, EditionServer, DBAccount


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'password',
        ]


class AdminSerializer(ModelSerializer):
    class Meta:
        model = Admin
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'password',
        ]


class TeacherSerializer(ModelSerializer):
    class Meta:
        model = Teacher
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'password',
        ]


class RoleSerializer(ModelSerializer):
    class Meta:
        model = Role
        fields = [
            'id',
            'name',
            'description',
        ]


class PermissionSerializer(ModelSerializer):
    class Meta:
        model = Permission
        fields = [
            'id',
            'name',
            'description',
        ]


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'id',
            'name',
            'description',
        ]


class SemesterSerializer(ModelSerializer):
    class Meta:
        model = Semester
        fields = [
            'id',
            'year',
            'winter',
        ]


class EditionSerializer(ModelSerializer):
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
    
    def to_representation(self, instance):
        self.fields['course'] = CourseSerializer(many=False, read_only=True)
        self.fields['semester'] = SemesterSerializer(many=False, read_only=True)
        return super(EditionSerializer, self).to_representation(instance)


class TeacherEditionSerializer(ModelSerializer):
    class Meta:
        model = TeacherEdition
        fields = [
            'id',
            'teacher',
            'edition',
        ]
    
    def to_representation(self, instance):
        self.fields['teacher'] = TeacherSerializer(many=False, read_only=True)
        self.fields['edition'] = EditionSerializer(many=False, read_only=True)
        return super(TeacherEditionSerializer, self).to_representation(instance)


class StudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'password',
            'student_id',
            'groups',
        ]


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = [
            'id',
            'name',
            'day',
            'hour',
            'room',
            'teacherEdition',
            'students',
        ]
    
    def to_representation(self, instance):
        self.fields['teacherEdition'] = TeacherEditionSerializer(many=False, read_only=True)
        self.fields['students'] = StudentSerializer(many=True, read_only=True)
        return super(GroupSerializer, self).to_representation(instance)


class ServerSerializer(ModelSerializer):
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


class EditionServerSerializer(ModelSerializer):
    class Meta:
        model = EditionServer
        fields = [
            'id',
            'edition',
            'server',
            'additional_info',
        ]
    
    def to_representation(self, instance):
        self.fields['edition'] = EditionSerializer(many=False, read_only=True)
        self.fields['server'] = ServerSerializer(many=False, read_only=True)
        return super(EditionServerSerializer, self).to_representation(instance)


class DBAccountSerializer(ModelSerializer):
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
    
    def to_representation(self, instance):
        self.fields['student'] = StudentSerializer(many=False, read_only=True)
        self.fields['editionServer'] = EditionServerSerializer(many=False, read_only=True)
        return super(DBAccountSerializer, self).to_representation(instance)