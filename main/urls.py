from django.urls import path
from dashboard.views import DashboardHomeView

app_name = 'main'

urlpatterns = [
    path('', DashboardHomeView.as_view(), name='dashboard'),
]
