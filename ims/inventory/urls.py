from django.urls import path
from . import views

urlpatterns = [
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('stock', views.stock, name='stock'),
    path('requisition', views.requisition, name='requisition'),
    path('employees', views.employees, name='employees'),
    path('try', views.trying, name='try'),
    path('profile', views.profile, name='profile')
]