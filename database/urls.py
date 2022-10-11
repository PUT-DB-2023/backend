from rest_framework import routers
from django.urls import path, include
from . import views

router =  routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('admins', views.AdminViewSet)
router.register('teachers', views.TeacherViewSet)
router.register('students', views.StudentViewSet)
router.register('roles', views.RoleViewSet)
router.register('permissions', views.PermissionViewSet)
router.register('courses', views.CourseViewSet)
router.register('semesters', views.SemesterViewSet)
router.register('editions', views.EditionViewSet)
router.register('teacher_editions', views.TeacherEditionViewSet)
router.register('groups', views.GroupViewSet)
router.register('servers', views.ServerViewSet)
router.register('edition_servers', views.EditionServerViewSet)
router.register('db_accounts', views.DBAccountViewSet)
# router.register('add_db_account', views.AddUserAccountToExternalDB)


urlpatterns = [
    path('api/', include(router.urls)),
    path('api/add_db_account', views.AddUserAccountToExternalDB.as_view({'post': 'add_db_account'})),
]