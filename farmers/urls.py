from django.urls import path
from . import views

app_name = 'farmers'

urlpatterns = [
    # Nông dân
    path('', views.FarmerListView.as_view(), name='list'),
    path('create/', views.FarmerCreateView.as_view(), name='create'),
    path('<int:pk>/', views.FarmerDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.FarmerUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.FarmerDeleteView.as_view(), name='delete'),
]
