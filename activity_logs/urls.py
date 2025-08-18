from django.urls import path
from . import views

app_name = 'activity_logs'

urlpatterns = [
    path('', views.ActivityLogListView.as_view(), name='list'),
    path('security/', views.SecurityEventListView.as_view(), name='security'),
]
