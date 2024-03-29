from rest_framework import routers
from django.urls import path, include
from . import views

router =  routers.DefaultRouter()
router.register('users', views.UserViewSet, basename='users')
router.register('teachers', views.TeacherViewSet, basename='teachers')
router.register('students', views.StudentViewSet, basename='students')
router.register('majors', views.MajorViewSet, basename='majors')
router.register('courses', views.CourseViewSet, basename='courses')
router.register('semesters', views.SemesterViewSet, basename='semesters')
router.register('editions', views.EditionViewSet, basename='editions')
router.register('teacher_editions', views.TeacherEditionViewSet, basename='teacher_editions')
router.register('groups', views.GroupViewSet, basename='groups')
router.register('dbms', views.DBMSViewSet, basename='dbms')
router.register('servers', views.ServerViewSet, basename='servers')
router.register('edition_servers', views.EditionServerViewSet, basename='edition_servers')
router.register('db_accounts', views.DBAccountViewSet, basename='db_accounts')
# router.register('basic_teacher_editions', views.SimpleTeacherEditionViewSet, basename='simple_teacher_editions')
# router.register('basic_semesters', views.SimpleSemesterViewSet, basename='simple_semesters')


urlpatterns = [
    path('', include(router.urls)),
    path('move_db_account', views.MoveDbAccount.as_view({'post': 'move_db_account'})),
    path('delete_db_account', views.RemoveUserFromExternalDB.as_view({'post': 'delete_db_account'})),
    path('load_students_csv', views.LoadStudentsFromCSV.as_view({'post': 'load_students_csv'})),
    path('change_active_semester', views.ChangeActiveSemester.as_view({'post': 'change_active_semester'})),
    path('add_students_to_group', views.AddStudentsToGroup.as_view({'post': 'add_students_to_group'})),
    path('remove_student_from_group', views.RemoveStudentFromGroup.as_view({'post': 'remove_student_from_group'})),
    path('login', views.LoginView.as_view({'post': 'login_user'})),
    path('logout', views.LogoutView.as_view({'post': 'logout_user'})),
    path('reset_own_password', views.ResetOwnPassword.as_view({'post': 'reset_own_password'})),
    path('reset_student_password', views.ResetStudentPassword.as_view({'post': 'reset_student_password'})),
    path('reset_teacher_password', views.ResetTeacherPassword.as_view({'post': 'reset_teacher_password'})),
    path('update_password_after_reset', views.UpdatePasswordAfterReset.as_view({'post': 'update_password_after_reset'})),
    path('reset_db_password', views.ResetDBPassword.as_view({'post': 'reset_db_password'})),
    path('delete_edition', views.DeleteEdition.as_view({'post': 'delete_edition'})),
    path('delete_students_without_groups', views.DeleteStudentsWithoutGroups.as_view({'post': 'delete_students_without_groups'})),
    path('execute_custom_command', views.ExecuteCustomCommand.as_view({'post': 'execute_custom_command'})),
]