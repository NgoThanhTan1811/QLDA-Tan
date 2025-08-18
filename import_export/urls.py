from django.urls import path
from . import views

app_name = 'import_export'

urlpatterns = [
    path('documents/', views.DocumentListView.as_view(), name='documents'),
    path('customs/', views.CustomsListView.as_view(), name='customs'),
]
