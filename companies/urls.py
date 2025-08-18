from django.urls import path
from . import views

app_name = 'companies'

urlpatterns = [
    path('', views.CompanyListView.as_view(), name='list'),
    path('create/', views.CompanyCreateView.as_view(), name='create'),
    path('<int:pk>/', views.CompanyDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.CompanyUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.CompanyDeleteView.as_view(), name='delete'),
    
    # API endpoints
    path('api/list/', views.CompanyAPIListView.as_view(), name='api_list'),
    path('api/create/', views.CompanyAPICreateView.as_view(), name='api_create'),
    path('api/<int:pk>/', views.CompanyAPIDetailView.as_view(), name='api_detail'),

]
