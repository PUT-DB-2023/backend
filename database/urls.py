from rest_framework import routers
from django.urls import path, include
from . import views

router =  routers.DefaultRouter()
router.register('users', views.UserViewSet, basename='users')
router.register('admins', views.AdminViewSet, basename='admins')
router.register('teachers', views.TeacherViewSet, basename='teachers')
router.register('students', views.StudentViewSet, basename='students')
router.register('roles', views.RoleViewSet, basename='roles')
router.register('permissions', views.PermissionViewSet, basename='permissions')
router.register('majors', views.MajorViewSet, basename='majors')
router.register('courses', views.CourseViewSet, basename='courses')
router.register('semesters', views.SemesterViewSet, basename='semesters')
router.register('editions', views.EditionViewSet, basename='editions')
router.register('teacher_editions', views.TeacherEditionViewSet, basename='teacher_editions')
router.register('groups', views.GroupViewSet, basename='groups')
router.register('servers', views.ServerViewSet, basename='servers')
router.register('edition_servers', views.EditionServerViewSet, basename='edition_servers')
router.register('db_accounts', views.DBAccountViewSet, basename='db_accounts')
router.register('basic_teacher_editions', views.SimpleTeacherEditionViewSet, basename='simple_teacher_editions')
router.register('basic_semesters', views.SimpleSemesterViewSet, basename='simple_semesters')


urlpatterns = [
    path('api/', include(router.urls)),
    path('api/add_db_account', views.AddUserAccountToExternalDB.as_view({'post': 'add_db_account'})),
    path('api/delete_db_account', views.RemoveUserFromExternalDB.as_view({'post': 'delete_db_account'})),
    path('api/load_students_csv', views.LoadStudentsFromCSV.as_view({'post': 'load_students_csv'})),
    path('api/change_active_semester', views.ChangeActiveSemester.as_view({'post': 'change_active_semester'})),
    path('api/add_student_to_group', views.AddStudentToGroup.as_view({'post': 'add_student_to_group'})),
    path('api/remove_student_from_group', views.RemoveStudentFromGroup.as_view({'post': 'remove_student_from_group'})),
]