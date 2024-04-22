from django.urls import path
from . import views

urlpatterns = [
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('employees', views.employees, name='employees'),
    path('stock/delete/<int:pk>/', views.stock_delete, name='stock-delete'),
    path('stock/update/<int:pk>/', views.stock_update, name='stock-update'),
    path('employees/detail/<int:pk>/', views.employees_detail, name='employees-detail'),
    path('update_order_status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('order/delete/<int:pk>/', views.delete_order, name='order-delete'),
    path('order/update/<int:pk>/', views.order_update, name='order-update'),
    path('searchdata', views.searchdata, name='searchdata'),
    path('searchdata2', views.searchdata2, name='searchdata2'),
    path('searchdata3', views.searchdata3, name='searchdata3'),
    path('report', views.report, name='report'),
    path('order_excel', views.order_excel, name='order_excel'),
    path('order_pdf', views.order_pdf, name='order_pdf'),
    path('instructions', views.instructions, name='instructions'),
    path('view_stock', views.viewstock, name='view-stock'),
    path('add_stock', views.addstock, name='add-stock'),
    path('view_request', views.viewrequest, name='view-request'),
    path('add_request/add', views.addrequest, name='add-request')
    
]