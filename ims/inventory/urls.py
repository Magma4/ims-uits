from django.urls import path
from . import views

urlpatterns = [
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('employees', views.employees, name='employees'),
    path('employees/detail/<int:pk>/', views.employees_detail, name='employees-detail'),
    path('update_order_status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('add_request/', views.OrderCreateView.as_view(), name='add-request'),
    path('update/<int:pk>', views.OrderUpdateView.as_view(), name='order-update'),
    path('delete/<int:pk>', views.OrderDeleteView.as_view(), name='order-delete'),
    path('searchdata', views.searchdata, name='searchdata'),
    path('searchdata2', views.searchdata2, name='searchdata2'),
    path('searchdata3', views.searchdata3, name='searchdata3'),
    path('report', views.report, name='report'),
    path('order_excel', views.order_excel, name='order_excel'),
    path('order_pdf', views.order_pdf, name='order_pdf'),
    path('instructions', views.instructions, name='instructions'),
    path('view_stock', views.viewstock, name='view-stock'),
    path('view_request', views.viewrequest, name='view-request'),
    path('add_stock/', views.StockCreateView.as_view(), name='add-stock'),
    path('stock/update/<int:pk>', views.StockUpdateView.as_view(), name='stock-update'),
    path('stock/delete/<int:pk>', views.StockDeleteView.as_view(), name='stock-delete'),
    path('celery', views.celery, name='celery')
    
]