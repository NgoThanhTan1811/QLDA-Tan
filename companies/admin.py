from django.contrib import admin
from .models import Company, CompanyDocument

class CompanyDocumentInline(admin.TabularInline):
    model = CompanyDocument
    extra = 1

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'company_type', 'tax_code', 'contact_person', 'is_active', 'created_at')
    list_filter = ('company_type', 'is_active', 'created_at')
    search_fields = ('name', 'tax_code', 'contact_person', 'email')
    ordering = ('name',)
    inlines = [CompanyDocumentInline]
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('name', 'company_type', 'tax_code', 'address', 'phone', 'email', 'website')
        }),
        ('Thông tin ngân hàng', {
            'fields': ('bank_name', 'bank_account'),
            'classes': ('collapse',)
        }),
        ('Thông tin liên hệ', {
            'fields': ('contact_person', 'contact_phone', 'contact_email')
        }),
        ('Giấy phép xuất nhập khẩu', {
            'fields': ('import_license', 'export_license'),
            'classes': ('collapse',)
        }),
        ('Trạng thái', {
            'fields': ('is_active',)
        })
    )

@admin.register(CompanyDocument)
class CompanyDocumentAdmin(admin.ModelAdmin):
    list_display = ('company', 'document_type', 'title', 'expiry_date', 'uploaded_at')
    list_filter = ('document_type', 'uploaded_at', 'expiry_date')
    search_fields = ('company__name', 'title')
    autocomplete_fields = ('company',)
