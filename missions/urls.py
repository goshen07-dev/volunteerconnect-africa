from django.urls import path
from . import views

urlpatterns = [
    path('', views.mission_list, name='mission_list'),
    path('<slug:slug>/', views.mission_detail, name='mission_detail'),
    path('<slug:slug>/postuler/', views.postuler, name='postuler'),
]