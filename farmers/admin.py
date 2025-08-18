from django.contrib import admin
from .models import Farmer, FarmingArea, CropProduct, FarmerDocument

class FarmingAreaInline(admin.TabularInline):
    model = FarmingArea
    extra = 0
    fields = ('area_name', 'area_size', 'soil_type', 'water_source')

class CropProductInline(admin.TabularInline):
    model = CropProduct
    extra = 0
    fields = ('product_name', 'variety', 'harvest_season', 'estimated_yield', 'price_per_kg', 'is_available')

class FarmerDocumentInline(admin.TabularInline):
    model = FarmerDocument
    extra = 0
    fields = ('document_type', 'title', 'file', 'expiry_date')

@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ('farmer_code', 'name', 'farmer_type', 'phone', 'province', 'certifications', 
                   'total_farm_area', 'rating', 'is_verified', 'is_active', 'created_at')
    list_filter = ('farmer_type', 'certifications', 'is_verified', 'is_active', 'is_featured', 
                  'province', 'created_at')
    search_fields = ('farmer_code', 'name', 'phone', 'email', 'tax_code', 'farming_region')
    readonly_fields = ('farmer_code', 'rating', 'total_reviews', 'created_at', 'updated_at')
    list_editable = ('is_verified', 'is_active')
    inlines = [FarmingAreaInline, CropProductInline, FarmerDocumentInline]
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('farmer_code', 'name', 'farmer_type', 'phone', 'email')
        }),
        ('Địa chỉ & Vùng canh tác', {
            'fields': ('province', 'district', 'ward', 'address', 'farming_region')
        }),
        ('Thông tin canh tác', {
            'fields': ('total_farm_area', 'active_farm_area', 'farming_experience', 'main_crops')
        }),
        ('Chứng nhận', {
            'fields': ('certifications', 'certification_number', 'certification_expiry')
        }),
        ('Thông tin ngân hàng', {
            'fields': ('bank_name', 'bank_account', 'account_holder'),
            'classes': ('collapse',)
        }),
        ('Thuế', {
            'fields': ('tax_code',),
            'classes': ('collapse',)
        }),
        ('Đánh giá', {
            'fields': ('rating', 'total_reviews'),
            'classes': ('collapse',)
        }),
        ('Trạng thái', {
            'fields': ('is_verified', 'is_active', 'is_featured')
        }),
        ('Thời gian', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(FarmingArea)
class FarmingAreaAdmin(admin.ModelAdmin):
    list_display = ('farmer', 'area_name', 'area_size', 'soil_type', 'water_source', 'created_at')
    list_filter = ('soil_type', 'water_source', 'created_at')
    search_fields = ('farmer__name', 'area_name', 'soil_type')

@admin.register(CropProduct)
class CropProductAdmin(admin.ModelAdmin):
    list_display = ('farmer', 'product_name', 'variety', 'harvest_season', 'quality_grade',
                   'estimated_yield', 'price_per_kg', 'is_organic', 'is_available', 'is_featured', 'expected_harvest_date')
    list_filter = ('harvest_season', 'quality_grade', 'is_organic', 'has_certificate', 
                  'is_available', 'is_featured', 'expected_harvest_date')
    search_fields = ('farmer__name', 'product_name', 'variety', 'certificate_type')
    date_hierarchy = 'expected_harvest_date'
    list_editable = ('is_available', 'is_featured')
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('farmer', 'farming_area', 'product_name', 'variety')
        }),
        ('Thời gian canh tác', {
            'fields': ('planting_date', 'harvest_season', 'expected_harvest_date', 'actual_harvest_date')
        }),
        ('Sản lượng & Chất lượng', {
            'fields': ('estimated_yield', 'actual_yield', 'quality_grade', 'price_per_kg', 'min_order_quantity')
        }),
        ('Chứng nhận', {
            'fields': ('is_organic', 'has_certificate', 'certificate_type')
        }),
        ('Mô tả', {
            'fields': ('description', 'growing_method', 'harvest_method', 'storage_method'),
            'classes': ('collapse',)
        }),
        ('Trạng thái', {
            'fields': ('is_available', 'is_featured')
        }),
    )

@admin.register(FarmerDocument)
class FarmerDocumentAdmin(admin.ModelAdmin):
    list_display = ('farmer', 'document_type', 'title', 'issue_date', 'expiry_date', 'uploaded_at')
    list_filter = ('document_type', 'uploaded_at', 'issue_date', 'expiry_date')
    search_fields = ('farmer__name', 'title', 'notes')
