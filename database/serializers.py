from rest_framework.serializers import ModelSerializer
from .models import User, Admin, Teacher, Student, Role, Permission, Major, Course, Semester, Edition, TeacherEdition, Group, Server, EditionServer, DBAccount


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'password',
            'roles',
        ]
    
    def to_representation(self, instance):
        self.fields['roles'] = BasicRoleSerializer(many=True, read_only=True)
        return super(UserSerializer, self).to_representation(instance)


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
            'editions',
        ]

    def to_representation(self, instance):
        self.fields['editions'] = BasicEditionSerializer(many=True, read_only=True)
        return super(TeacherSerializer, self).to_representation(instance)


class BasicTeacherSerializer(ModelSerializer):
    class Meta:
        model = Teacher
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'password',
        ]


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
            'db_accounts',
        ]
    
    def to_representation(self, instance):
        self.fields['groups'] = BasicGroupSerializer(many=True, read_only=True)
        self.fields['db_accounts'] = BasicDBAccountSerializer(many=True, read_only=True)
        return super(StudentSerializer, self).to_representation(instance)


class BasicStudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'password',
            'student_id',
        ]


class RoleSerializer(ModelSerializer):
    class Meta:
        model = Role
        fields = [
            'id',
            'name',
            'description',
            'permissions',
            'users',
        ]
    
    def to_representation(self, instance):
        self.fields['permissions'] = BasicPermissionSerializer(many=True, read_only=True)
        # self.fields['users'] = UserSerializer(many=True, read_only=True)
        return super(RoleSerializer, self).to_representation(instance)


class BasicRoleSerializer(ModelSerializer):
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
            'roles',
        ]
    
    def to_representation(self, instance):
        self.fields['roles'] = BasicRoleSerializer(many=True, read_only=True)
        return super(PermissionSerializer, self).to_representation(instance)


class BasicPermissionSerializer(ModelSerializer):
    class Meta:
        model = Permission
        fields = [
            'id',
            'name',
            'description',
        ]


class MajorSerializer(ModelSerializer):
    class Meta:
        model = Major
        fields = [
            'id',
            'name',
            'description',
            'courses',
        ]
    
    def to_representation(self, instance):
        self.fields['courses'] = BasicCourseSerializer(many=True, read_only=True)
        return super(MajorSerializer, self).to_representation(instance)


class BasicMajorSerializer(ModelSerializer):
    class Meta:
        model = Major
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
            'active',
            'major',
        ]
    
    def to_representation(self, instance):
        self.fields['major'] = BasicMajorSerializer(read_only=True)
        return super(CourseSerializer, self).to_representation(instance)


class BasicCourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'id',
            'name',
            'description',
            'active',
        ]


class SemesterSerializer(ModelSerializer):
    class Meta:
        model = Semester
        fields = [
            'id',
            'year',
            'winter',
            'active',
            'editions',
        ]
    
    def to_representation(self, instance):
        self.fields['editions'] = EditionSerializerForSemester(many=True, read_only=True)
        return super(SemesterSerializer, self).to_representation(instance)


class BasicSemesterSerializer(ModelSerializer):
    class Meta:
        model = Semester
        fields = [
            'id',
            'year',
            'winter',
            'active',
        ]

class EditionSerializer(ModelSerializer):
    class Meta:
        model = Edition
        fields = [
            'id',
            'description',
            'date_opened',
            'date_closed',
            'semester',
            'course',
            'teachers',
            'servers',
        ]
    
    def to_representation(self, instance):
        self.fields['course'] = CourseSerializer(many=False, read_only=True)
        self.fields['semester'] = BasicSemesterSerializer(many=False, read_only=True)
        self.fields['teachers'] = BasicTeacherSerializer(many=True, read_only=True)
        self.fields['servers'] = ServerSerializer(many=True, read_only=True)
        return super(EditionSerializer, self).to_representation(instance)


class BasicEditionSerializer(ModelSerializer):
    class Meta:
        model = Edition
        fields = [
            'id',
            'semester',
            'course',
            'servers',
        ]
    
    def to_representation(self, instance):
        self.fields['semester'] = BasicSemesterSerializer(many=False, read_only=True)
        self.fields['course'] = CourseSerializer(many=False, read_only=True)
        self.fields['servers'] = ServerSerializer(many=True, read_only=True)
        return super(BasicEditionSerializer, self).to_representation(instance)


class EditionSerializerForSemester(ModelSerializer):
    class Meta:
        model = Edition
        fields = [
            'id',
            'course',
        ]
    
    def to_representation(self, instance):
        self.fields['course'] = BasicCourseSerializer(many=False, read_only=True)
        return super(EditionSerializerForSemester, self).to_representation(instance)


class BasicEditionSerializer(ModelSerializer):
    class Meta:
        model = Edition
        fields = [
            'id',
            'semester',
            'course',
        ]
    
    def to_representation(self, instance):
        self.fields['semester'] = BasicSemesterSerializer(many=False, read_only=True)
        self.fields['course'] = BasicCourseSerializer(many=False, read_only=True)
        return super(BasicEditionSerializer, self).to_representation(instance)


class TeacherEditionSerializer(ModelSerializer):
    class Meta:
        model = TeacherEdition
        fields = [
            'id',
            'teacher',
            'edition',
        ]
    
    def to_representation(self, instance):
        self.fields['teacher'] = BasicTeacherSerializer(many=False, read_only=True)
        self.fields['edition'] = BasicEditionSerializer(many=False, read_only=True)
        return super(TeacherEditionSerializer, self).to_representation(instance)


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
        self.fields['students'] = BasicStudentSerializer(many=True, read_only=True)
        return super(GroupSerializer, self).to_representation(instance)


class BasicGroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = [
            'id',
            'name',
            'day',
            'hour',
            'room',
            'teacherEdition',
        ]


class ServerSerializer(ModelSerializer):
    class Meta:
        model = Server
        fields = [
            'id',
            'name',
            'ip',
            'port',
            'provider',
            'user',
            'password',
            'database',
            'date_created',
            'create_user_template',
            'modify_user_template',
            'delete_user_template',
            'active',
        ]


class BasicServerSerializer(ModelSerializer):
    class Meta:
        model = Server
        fields = [
            'id',
            'name',
            'provider',
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
            'username_template',
            'passwd_template',
        ]
    
    def to_representation(self, instance):
        self.fields['edition'] = BasicEditionSerializer(many=False, read_only=True)
        self.fields['server'] = ServerSerializer(many=False, read_only=True)
        return super(EditionServerSerializer, self).to_representation(instance)


class BasicEditionServerSerializer(ModelSerializer):
    class Meta:
        model = EditionServer
        fields = [
            'id',
            'edition',
            'server',
        ]
    
    def to_representation(self, instance):
        self.fields['edition'] = BasicEditionSerializer(many=False, read_only=True)
        self.fields['server'] = BasicServerSerializer(many=False, read_only=True)
        return super(BasicEditionServerSerializer, self).to_representation(instance)


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
            'is_moved'
        ]
    
    def to_representation(self, instance):
        self.fields['student'] = BasicStudentSerializer(many=False, read_only=True)
        self.fields['editionServer'] = BasicEditionServerSerializer(many=False, read_only=True)
        return super(DBAccountSerializer, self).to_representation(instance)


class BasicDBAccountSerializer(ModelSerializer):
    class Meta:
        model = DBAccount
        fields = [
            'id',
            'username',
            'password',
            'additional_info',
            'editionServer',
            'is_moved'
        ]
    
    def to_representation(self, instance):
        self.fields['editionServer'] = BasicEditionServerSerializer(many=False, read_only=True)
        return super(BasicDBAccountSerializer, self).to_representation(instance)