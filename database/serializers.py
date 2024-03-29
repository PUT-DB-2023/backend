from rest_framework.serializers import ModelSerializer
from .models import User, Teacher, Student, Major, Course, Semester, Edition, TeacherEdition, Group, DBMS, Server, EditionServer, DBAccount


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'is_student',
            'is_teacher',
            'is_active',
            'is_superuser',
        ]


class TeacherSerializer(ModelSerializer):
    class Meta:
        model = Teacher
        fields = [
            'id',
            'user',
        ]

    def to_representation(self, instance):
        self.fields['user'] = UserSerializer(read_only=True)
        return super(TeacherSerializer, self).to_representation(instance)


class DetailedTeacherSerializer(ModelSerializer):
    class Meta:
        model = Teacher
        fields = [
            'id',
            'user',
            'editions',
        ]
    
    def to_representation(self, instance):
        self.fields['user'] = UserSerializer(read_only=True)
        self.fields['editions'] = BasicEditionSerializer(many=True, read_only=True)
        return super(DetailedTeacherSerializer, self).to_representation(instance)


class BasicTeacherSerializer(ModelSerializer):
    class Meta:
        model = Teacher
        fields = [
            'id',
            'user',
        ]
    
    def to_representation(self, instance):
        self.fields['user'] = UserSerializer(read_only=True)
        return super(BasicTeacherSerializer, self).to_representation(instance)


class StudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'id',
            'user',
            'student_id',
            'major',
            # 'groups',
            # 'db_accounts',
        ]
    
    def to_representation(self, instance):
        self.fields['user'] = UserSerializer(read_only=True)
        self.fields['major'] = BasicMajorSerializer(read_only=True)
        # self.fields['groups'] = BasicGroupSerializer(many=True, read_only=True)
        # self.fields['db_accounts'] = BasicDBAccountSerializer(many=True, read_only=True)
        return super(StudentSerializer, self).to_representation(instance)
    

class DetailedStudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'id',
            'user',
            'student_id',
            'major',
            'groups',
            'db_accounts',
        ]
    
    def to_representation(self, instance):
        self.fields['user'] = UserSerializer(read_only=True)
        self.fields['major'] = BasicMajorSerializer(read_only=True)
        self.fields['groups'] = GroupSerializerForStudent(many=True, read_only=True)
        self.fields['db_accounts'] = BasicDBAccountSerializer(many=True, read_only=True)
        return super(DetailedStudentSerializer, self).to_representation(instance)


class BasicStudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'id',
            'user',
            'student_id',
        ]
    
    def to_representation(self, instance):
        self.fields['user'] = UserSerializer(read_only=True)
        return super(BasicStudentSerializer, self).to_representation(instance)


class MajorSerializer(ModelSerializer):
    class Meta:
        model = Major
        fields = [
            'id',
            'name',
            'description',
            'courses',
            'students',
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
            'start_year',
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
            'start_year',
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
    
    # def create(self, validated_data):
    #     print(validated_data)
    #     teachers = validated_data.pop('teachers')
    #     edition = Edition.objects.create(**validated_data)
    #     for teacher in teachers:
    #         TeacherEdition.objects.create(teacher=teacher, edition=edition)
    #     return edition

    def to_representation(self, instance):
        self.fields['course'] = CourseSerializer(many=False, read_only=True)
        self.fields['semester'] = BasicSemesterSerializer(many=False, read_only=True)
        self.fields['teachers'] = TeacherSerializer(many=True, read_only=True)
        self.fields['servers'] = BasicServerSerializer(many=True, read_only=True)
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


class EditionSerializerForTeacherEdition(ModelSerializer):
    class Meta:
        model = Edition
        fields = [
            'id',
            'semester',
            'course',
            'servers',
        ]
    
    def to_representation(self, instance):
        self.fields['course'] = BasicCourseSerializer(many=False, read_only=True)
        self.fields['semester'] = BasicSemesterSerializer(many=False, read_only=True)
        self.fields['servers'] = BasicServerSerializer(many=True, read_only=True)
        return super(EditionSerializerForTeacherEdition, self).to_representation(instance)


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
        self.fields['edition'] = EditionSerializerForTeacherEdition(many=False, read_only=True)
        return super(TeacherEditionSerializer, self).to_representation(instance)


class BasicTeacherEditionSerializer(ModelSerializer):
    class Meta:
        model = TeacherEdition
        fields = [
            'id',
            'teacher',
        ]
    
    def to_representation(self, instance):
        self.fields['teacher'] = TeacherSerializer(many=False, read_only=True)
        return super(BasicTeacherEditionSerializer, self).to_representation(instance)


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
            # 'students',
        ]
    
    def to_representation(self, instance):
        self.fields['teacherEdition'] = TeacherEditionSerializer(many=False, read_only=True)
        # self.fields['students'] = BasicStudentSerializer(many=True, read_only=True)
        return super(GroupSerializer, self).to_representation(instance)


class DetailedGroupSerializer(ModelSerializer):
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
        return super(DetailedGroupSerializer, self).to_representation(instance)


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


class GroupSerializerForStudent(ModelSerializer):
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
    
    def to_representation(self, instance):
        self.fields['teacherEdition'] = TeacherEditionSerializer(many=False, read_only=True)
        return super(GroupSerializerForStudent, self).to_representation(instance)


class DBMSSerializer(ModelSerializer):
    class Meta:
        model = DBMS
        fields = [
            'id',
            'name',
            'description',
            'servers',
        ]
    
    def to_representation(self, instance):
        self.fields['servers'] = ServerSerializerForDBMS(many=True, read_only=True)
        return super(DBMSSerializer, self).to_representation(instance)


class BasicDBMSSerializer(ModelSerializer):
    class Meta:
        model = DBMS
        fields = [
            'id',
            'name',
            'description',
        ]


class ServerSerializer(ModelSerializer):
    class Meta:
        model = Server
        fields = [
            'id',
            'name',
            'host',
            'port',
            'dbms',
            'user',
            'password',
            'database',
            'date_created',
            # 'editions',
            'create_user_template',
            'modify_user_template',
            'delete_user_template',
            'custom_command_template',
            'username_template',
            'active',
        ]

    # def to_representation(self, instance):
    #     self.fields['editions'] = BasicEditionSerializer(many=True, read_only=True)
    #     return super(ServerSerializer, self).to_representation(instance)

    def to_representation(self, instance):
        self.fields['dbms'] = BasicDBMSSerializer(many=False, read_only=True)
        return super(ServerSerializer, self).to_representation(instance)

class BasicServerSerializer(ModelSerializer):
    class Meta:
        model = Server
        fields = [
            'id',
            'name',
            'dbms',
            'active',
        ]
    
    def to_representation(self, instance):
        self.fields['dbms'] = BasicDBMSSerializer(many=False, read_only=True)
        return super(BasicServerSerializer, self).to_representation(instance)


class ServerSerializerForDBMS(ModelSerializer):
    class Meta:
        model = Server
        fields = [
            'id',
            'name',
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