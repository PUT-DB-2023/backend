from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.UserViewSet.as_view({'get': 'list'}))
]
