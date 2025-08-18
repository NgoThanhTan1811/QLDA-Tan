from django.contrib import admin
from .models import Category, Unit, Product, ProductImage, ProductSpecification

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'description')
    search_fields = ('name', 'symbol')

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'category', 'origin', 'quality_grade', 'cost_price', 'selling_price', 'is_active')
    list_filter = ('category', 'origin', 'quality_grade', 'is_active', 'created_at')
    search_fields = ('code', 'name', 'description', 'hs_code')
    ordering = ('name',)
    inlines = [ProductImageInline, ProductSpecificationInline]
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('code', 'name', 'category', 'unit', 'description', 'image')
        }),
        ('Thông tin xuất xứ', {
            'fields': ('origin', 'origin_country', 'quality_grade')
        }),
        ('Thông tin giá', {
            'fields': ('cost_price', 'selling_price', 'export_price')
        }),
        ('Thông tin kỹ thuật', {
            'fields': ('shelf_life_days', 'storage_temperature_min', 'storage_temperature_max', 'humidity_requirement'),
            'classes': ('collapse',)
        }),
        ('Thông tin xuất nhập khẩu', {
            'fields': ('hs_code', 'tax_rate'),
            'classes': ('collapse',)
        }),
        ('Trạng thái', {
            'fields': ('is_active',)
        })
    )

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'caption', 'is_main', 'created_at')
    list_filter = ('is_main', 'created_at')
    search_fields = ('product__name', 'caption')

@admin.register(ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'value', 'unit')
    search_fields = ('product__name', 'name', 'value')
