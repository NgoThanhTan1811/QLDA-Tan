from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('', views.PaymentListView.as_view(), name='list'),
    path('create/', views.PaymentCreateView.as_view(), name='create'),
    path('<int:pk>/', views.PaymentDetailView.as_view(), name='detail'),
    path('<int:pk>/confirm/', views.PaymentConfirmView.as_view(), name='confirm'),
    path('<int:pk>/print/', views.PaymentPrintView.as_view(), name='print'),
]
