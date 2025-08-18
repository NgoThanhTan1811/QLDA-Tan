from django.contrib import admin
from .models import Customer, CustomerAddress, CustomerReview, CustomerWishlist, CustomerDocument

class CustomerAddressInline(admin.TabularInline):
    model = CustomerAddress
    extra = 0
    fields = ('address_type', 'recipient_name', 'phone', 'province', 'district', 'is_default')

class CustomerDocumentInline(admin.TabularInline):
    model = CustomerDocument
    extra = 0
    fields = ('document_type', 'title', 'file', 'expiry_date')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_code', 'full_name', 'customer_type', 'phone', 'email', 'membership_level', 
                   'total_orders', 'total_spent', 'is_vip', 'is_active', 'is_verified', 'created_at')
    list_filter = ('customer_type', 'membership_level', 'is_active', 'is_verified', 'is_vip', 
                  'province', 'created_at')
    search_fields = ('customer_code', 'full_name', 'phone', 'email', 'tax_code', 'company_name')
    readonly_fields = ('customer_code', 'total_orders', 'total_spent', 'average_order_value', 
                      'first_order_date', 'last_order_date', 'created_at', 'updated_at')
    list_editable = ('is_active', 'is_verified', 'is_vip')
    inlines = [CustomerAddressInline, CustomerDocumentInline]
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('user', 'customer_code', 'full_name', 'customer_type', 'phone', 'email')
        }),
        ('Địa chỉ', {
            'fields': ('province', 'district', 'ward', 'address')
        }),
        ('Thông tin doanh nghiệp', {
            'fields': ('company_name', 'tax_code', 'business_license'),
            'classes': ('collapse',)
        }),
        ('Thông tin thanh toán', {
            'fields': ('bank_name', 'bank_account', 'account_holder'),
            'classes': ('collapse',)
        }),
        ('Thành viên & Ưu đãi', {
            'fields': ('membership_level', 'points', 'credit_limit')
        }),
        ('Sở thích', {
            'fields': ('preferred_products', 'preferred_payment_method', 'preferred_delivery_time'),
            'classes': ('collapse',)
        }),
        ('Thống kê', {
            'fields': ('total_orders', 'total_spent', 'average_order_value', 'customer_rating'),
            'classes': ('collapse',)
        }),
        ('Thời gian', {
            'fields': ('date_of_birth', 'first_order_date', 'last_order_date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Trạng thái', {
            'fields': ('is_active', 'is_verified', 'is_vip')
        }),
    )

@admin.register(CustomerAddress)
class CustomerAddressAdmin(admin.ModelAdmin):
    list_display = ('customer', 'address_type', 'recipient_name', 'phone', 'province', 'is_default', 'created_at')
    list_filter = ('address_type', 'is_default', 'province', 'created_at')
    search_fields = ('customer__full_name', 'recipient_name', 'phone', 'address')

@admin.register(CustomerReview)
class CustomerReviewAdmin(admin.ModelAdmin):
    list_display = ('customer', 'farmer', 'rating', 'title', 'product_quality', 'delivery_time', 
                   'service_quality', 'is_verified', 'is_featured', 'created_at')
    list_filter = ('rating', 'product_quality', 'delivery_time', 'service_quality', 
                  'is_verified', 'is_featured', 'created_at')
    search_fields = ('customer__full_name', 'farmer__name', 'title', 'content')
    readonly_fields = ('created_at',)
    list_editable = ('is_verified', 'is_featured')
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('customer', 'farmer', 'order', 'rating')
        }),
        ('Nội dung đánh giá', {
            'fields': ('title', 'content')
        }),
        ('Đánh giá chi tiết', {
            'fields': ('product_quality', 'delivery_time', 'service_quality')
        }),
        ('Trạng thái', {
            'fields': ('is_verified', 'is_featured')
        }),
    )

@admin.register(CustomerWishlist)
class CustomerWishlistAdmin(admin.ModelAdmin):
    list_display = ('customer', 'farmer', 'product', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('customer__full_name', 'farmer__name', 'product__product_name')

@admin.register(CustomerDocument)
class CustomerDocumentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'document_type', 'title', 'issue_date', 'expiry_date', 'uploaded_at')
    list_filter = ('document_type', 'uploaded_at', 'issue_date', 'expiry_date')
    search_fields = ('customer__full_name', 'title', 'notes')
