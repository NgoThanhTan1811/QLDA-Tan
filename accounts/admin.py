from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active_employee', 'is_staff')
    list_filter = ('role', 'is_active_employee', 'is_staff', 'is_superuser', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone')
    ordering = ('-created_at',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Thông tin bổ sung', {
            'fields': ('phone', 'address', 'role', 'avatar', 'is_active_employee')
        }),
        ('Thời gian', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'department', 'position', 'hire_date')
    list_filter = ('department', 'hire_date')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'employee_id')
    autocomplete_fields = ('user',)
