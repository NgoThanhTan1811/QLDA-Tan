from django.contrib import admin
from .models import Customer, CustomerAddress

class CustomerAddressInline(admin.TabularInline):
    model = CustomerAddress
    extra = 0
    fields = ( 'recipient_name', 'phone', 'province', 'district', 'is_default')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_code', 'full_name', 'phone', 'email', 'is_active', 'is_verified', 'created_at')
    list_filter = ( 'is_active', 'is_verified', 'province', 'created_at')
    search_fields = ('customer_code', 'full_name', 'phone', 'email')
    readonly_fields = ( 'created_at', 'updated_at')
    list_editable = ('is_active', 'is_verified',)
    inlines = [CustomerAddressInline]
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('user', 'customer_code', 'full_name', 'phone', 'email')
        }),
        ('Địa chỉ', {
            'fields': ('province', 'district', 'ward', 'address')
        }),
        ('Thời gian', {
            'fields': ('date_of_birth', 'first_order_date', 'last_order_date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Trạng thái', {
            'fields': ('is_active', 'is_verified')
        }),
    )

@admin.register(CustomerAddress)
class CustomerAddressAdmin(admin.ModelAdmin):
    list_display = ( 'recipient_name', 'phone', 'province', 'is_default', 'created_at')
    list_filter = ('is_default', 'province', 'created_at')
    search_fields = ('customer__full_name', 'recipient_name', 'phone', 'address')
