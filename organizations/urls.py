from django.urls import path
from . import views

urlpatterns = [
    path('', views.organization_list,
         name='organization_list'),
    path('register/', views.organization_register,
         name='organization_register'),
    path('dashboard/', views.organization_dashboard,
         name='organization_dashboard'),
    path('mission/creer/', views.mission_create,
         name='mission_create'),
]