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
    path('update_order_status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('order/delete/<int:pk>/', views.delete_order, name='order-delete'),
    path('order/update/<int:pk>/', views.order_update, name='order-update'),
     
]