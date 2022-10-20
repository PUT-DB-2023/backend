from django_filters import rest_framework as filters

from backend.database.models import User, Admin, Teacher, Student, Permission, Role, Major, Course, Semester, Edition, TeacherEdition

class CourseFilter(filters.FilterSet):
    has_active_editions = filters.BooleanFilter(field_name='editions', method='filter_has_active_editions')

    class Meta:
        model = Course
        fields = ['name', 'major', 'description']