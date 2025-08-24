from django.contrib import admin
from .models import Employee, Customer


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'full_name', 'email', 'department', 'position', 'is_active', 'hire_date']
    list_filter = ['department', 'position', 'is_active', 'hire_date']
    search_fields = ['employee_id', 'first_name', 'last_name', 'email', 'phone']
    readonly_fields = ['full_name', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('employee_id', 'first_name', 'last_name', 'nickname', 'full_name')
        }),
        ('Thông tin cá nhân', {
            'fields': ('gender', 'date_of_birth', 'national_id', 'avatar')
        }),
        ('Thông tin liên hệ', {
            'fields': ('email', 'phone', 'address', 'emergency_contact_name', 'emergency_contact_phone')
        }),
        ('Thông tin công việc', {
            'fields': ('department', 'position', 'hire_date', 'salary', 'job_description')
        }),
        ('Thông tin bổ sung', {
            'fields': ('education_level', 'marital_status', 'bank_account', 'bank_name')
        }),
        ('Trạng thái', {
            'fields': ('is_active', 'notes')
        }),
        ('Thời gian', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['customer_code', 'name', 'email', 'phone', 'avatar', 'is_active', 'address']
    search_fields = ['customer_code', 'name', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('customer_code', 'name', 'email', 'phone', 'avatar', 'address')
        }),
        ('Trạng thái', {
            'fields': ('is_active', 'notes')
        }),
        ('Thời gian', {
            'fields': ('created_at', 'updated_at'),
        })
    )
