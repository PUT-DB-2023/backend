from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import UserSerializer, AdminSerializer, TeacherSerializer, StudentSerializer, RoleSerializer, UserRoleSerializer, PermissionSerializer, RolePermissionSerializer, CourseSerializer, SemesterSerializer, EditionSerializer, TeacherEditionSerializer, GroupSerializer, ServerSerializer, EditionServerSerializer, StudentGroupSerializer, DBAccountSerializer
from .models import User, Admin, Teacher, Student, Role, UserRole, Permission, RolePermission, Course, Semester, Edition, TeacherEdition, Group, Server, EditionServer, StudentGroup, DBAccount
from django.shortcuts import get_object_or_404


class UserViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()

    # def list(self, request):
    #     queryset = User.objects.all()
    #     serializer = UserSerializer(queryset, many=True)
    #     return Response(serializer.data)

    # def retrieve(self, request, pk=None):
    #     queryset = User.objects.all()
    #     user = get_object_or_404(queryset, pk=pk)
    #     serializer = UserSerializer(user)
    #     return Response(serializer.data)

class AdminViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving admins.
    """
    serializer_class = AdminSerializer
    queryset = Admin.objects.all()

class TeacherViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving teachers.
    """
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()

class StudentViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving students.
    """
    serializer_class = StudentSerializer
    queryset = Student.objects.all()

class RoleViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving roles.
    """
    serializer_class = RoleSerializer
    queryset = Role.objects.all()

class UserRoleViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving user roles.
    """
    serializer_class = UserRoleSerializer
    queryset = UserRole.objects.all()

class PermissionViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving permissions.
    """
    serializer_class = PermissionSerializer
    queryset = Permission.objects.all()

class RolePermissionViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving role permissions.
    """
    serializer_class = RolePermissionSerializer
    queryset = RolePermission.objects.all()

class CourseViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving courses.
    """
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

class SemesterViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving semesters.
    """
    serializer_class = SemesterSerializer
    queryset = Semester.objects.all()

class EditionViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving editions.
    """
    serializer_class = EditionSerializer
    queryset = Edition.objects.all()

class TeacherEditionViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving teacher editions.
    """
    serializer_class = TeacherEditionSerializer
    queryset = TeacherEdition.objects.all()

class GroupViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving groups.
    """
    serializer_class = GroupSerializer
    queryset = Group.objects.all()

class ServerViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving servers.
    """
    serializer_class = ServerSerializer
    queryset = Server.objects.all()

class EditionServerViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving edition servers.
    """
    serializer_class = EditionServerSerializer
    queryset = EditionServer.objects.all()

class StudentGroupViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving student groups.
    """
    serializer_class = StudentGroupSerializer
    queryset = StudentGroup.objects.all()

class DBAccountViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving db accounts.
    """
    serializer_class = DBAccountSerializer
    queryset = DBAccount.objects.all()