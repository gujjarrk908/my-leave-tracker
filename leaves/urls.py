from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add/', views.add_leave, name='add_leave'),
    path('edit/<int:pk>/', views.edit_leave, name='edit_leave'),
]
