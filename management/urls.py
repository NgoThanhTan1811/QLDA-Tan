from django.urls import path
from . import views

app_name = 'management'

urlpatterns = [
    # Management home
    path('', views.ManagementIndexView.as_view(), name='index'),
    
    # Employee URLs
    path('employees/', views.EmployeeListView.as_view(), name='employee_list'),
    path('employees/create/', views.EmployeeCreateView.as_view(), name='employee_create'),
    path('employees/<int:pk>/', views.EmployeeDetailView.as_view(), name='employee_detail'),
    path('employees/<int:pk>/edit/', views.EmployeeUpdateView.as_view(), name='employee_edit'),
    path('employees/<int:pk>/delete/', views.EmployeeDeleteView.as_view(), name='employee_delete'),
    
    # Farmer URLs
    path('farmers/', views.FarmerListView.as_view(), name='farmer_list'),
    path('farmers/create/', views.FarmerCreateView.as_view(), name='farmer_create'),
    path('farmers/<int:pk>/', views.FarmerDetailView.as_view(), name='farmer_detail'),
    path('farmers/<int:pk>/edit/', views.FarmerUpdateView.as_view(), name='farmer_edit'),
    path('farmers/<int:pk>/delete/', views.FarmerDeleteView.as_view(), name='farmer_delete'),
    
    # Customer URLs
    path('customers/', views.CustomerListView.as_view(), name='customer_list'),
    path('customers/create/', views.CustomerCreateView.as_view(), name='customer_create'),
    path('customers/<int:pk>/', views.CustomerDetailView.as_view(), name='customer_detail'),
    path('customers/<int:pk>/edit/', views.CustomerUpdateView.as_view(), name='customer_edit'),
    path('customers/<int:pk>/delete/', views.CustomerDeleteView.as_view(), name='customer_delete'),
    
    # Export/Import URLs
    path('export/<str:data_type>/', views.export_data, name='export_data'),
    path('import/', views.import_data, name='import_data'),
]
