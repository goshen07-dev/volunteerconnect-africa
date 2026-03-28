from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='volunteer_register'),
    path('login/', views.login_view, name='volunteer_login'),
    path('logout/', views.logout_view, name='volunteer_logout'),
    path('dashboard/', views.dashboard, name='volunteer_dashboard'),
    path('profil/modifier/', views.profile_edit, name='volunteer_profile_edit'),
]