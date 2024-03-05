from django.urls import path
from . import views

urlpatterns = [
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('stock', views.stock, name='stock'),
    path('requisition', views.requisition, name='requisition'),
    path('employees', views.employees, name='employees'),
    path('stock/delete/<int:pk>/', views.stock_delete, name='stock-delete'),
    path('stock/update/<int:pk>/', views.stock_update, name='stock-update'),
    path('employees/detail/<int:pk>/', views.employees_detail, name='employees-detail'),
]