from rest_framework import routers
from django.urls import path, include
from . import views

router =  routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('admins', views.AdminViewSet)
router.register('teachers', views.TeacherViewSet)
router.register('students', views.StudentViewSet)
router.register('roles', views.RoleViewSet)
router.register('user_roles', views.UserRoleViewSet)
router.register('permissions', views.PermissionViewSet)
router.register('role_permissions', views.RolePermissionViewSet)
router.register('courses', views.CourseViewSet)
router.register('semesters', views.SemesterViewSet)
router.register('editions', views.EditionViewSet)
router.register('teacher_editions', views.TeacherEditionViewSet)
router.register('groups', views.GroupViewSet)
router.register('servers', views.ServerViewSet)
router.register('edition_servers', views.EditionServerViewSet)
router.register('student_groups', views.StudentGroupViewSet)
router.register('db_accounts', views.DBAccountViewSet)
# router.register('docs', views.DocsViewSet)


try:
    urlpatterns = [
        path('api/', include(router.urls)),
        # path('docs', views.schema_view)
        # views.UserViewSet.as_view({'get': 'list'})
    ]
except:
    urlpatterns = []
