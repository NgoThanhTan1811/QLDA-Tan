from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
    # path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),  # Removed as requested
    path('update-profile/', views.update_profile, name='update_profile'),
    path('update-notifications/', views.update_notifications, name='update_notifications'),
    path('update-preferences/', views.update_preferences, name='update_preferences'),
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/companies/', views.CompanyUserListView.as_view(), name='company_users'),
    path('users/admin/', views.AdminUserListView.as_view(), name='admin_users'),
    path('users/customers/', views.CustomerUserListView.as_view(), name='customer_users'),
    path('users/create/', views.create_user, name='create_user'),
    path('user/<int:user_id>/delete/', views.delete_user, name='delete_user'),
]
