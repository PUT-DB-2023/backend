from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.PersonViewSet.as_view({'get': 'list'}))
]
