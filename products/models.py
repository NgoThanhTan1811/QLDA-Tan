from django.db import models
from django.core.validators import MinValueValidator

class Category(models.Model):
    """Danh mục trái cây"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Tên danh mục")
    description = models.TextField(blank=True, verbose_name="Mô tả")
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name="Hình ảnh")
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    
    class Meta:
        verbose_name = "Danh mục"
        verbose_name_plural = "Danh mục"
        ordering = ['name']
        
    def __str__(self):
        return self.name

class Unit(models.Model):
    """Đơn vị tính"""
    name = models.CharField(max_length=50, unique=True, verbose_name="Tên đơn vị")
    symbol = models.CharField(max_length=10, verbose_name="Ký hiệu")
    description = models.TextField(blank=True, verbose_name="Mô tả")
    
    class Meta:
        verbose_name = "Đơn vị tính"
        verbose_name_plural = "Đơn vị tính"
        ordering = ['name']
        
    def __str__(self):
        return f"{self.name} ({self.symbol})"

class Product(models.Model):
    """Model sản phẩm trái cây"""
    ORIGIN_CHOICES = [
        ('domestic', 'Trong nước'),
        ('imported', 'Nhập khẩu'),
    ]
    
    QUALITY_GRADE_CHOICES = [
        ('A', 'Loại A (Xuất khẩu)'),
        ('B', 'Loại B (Nội địa cao cấp)'),
        ('C', 'Loại C (Nội địa thường)'),
    ]
    
    code = models.CharField(max_length=20, unique=True, verbose_name="Mã sản phẩm")
    name = models.CharField(max_length=200, verbose_name="Tên sản phẩm")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Danh mục")
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, verbose_name="Đơn vị tính")
    
    # Thông tin cơ bản
    description = models.TextField(blank=True, verbose_name="Mô tả")
    origin = models.CharField(max_length=20, choices=ORIGIN_CHOICES, verbose_name="Xuất xứ")
    origin_country = models.CharField(max_length=100, blank=True, verbose_name="Quốc gia xuất xứ")
    quality_grade = models.CharField(max_length=5, choices=QUALITY_GRADE_CHOICES, verbose_name="Phân loại chất lượng")
    
    # Thông tin giá
    cost_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Giá vốn")
    selling_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Giá bán")
    export_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], blank=True, null=True, verbose_name="Giá xuất khẩu")
    
    # Thông tin kỹ thuật
    shelf_life_days = models.PositiveIntegerField(verbose_name="Hạn sử dụng (ngày)")
    storage_temperature_min = models.FloatField(blank=True, null=True, verbose_name="Nhiệt độ bảo quản tối thiểu (°C)")
    storage_temperature_max = models.FloatField(blank=True, null=True, verbose_name="Nhiệt độ bảo quản tối đa (°C)")
    humidity_requirement = models.CharField(max_length=50, blank=True, verbose_name="Yêu cầu độ ẩm")
    
    # Thông tin xuất nhập khẩu
    hs_code = models.CharField(max_length=20, blank=True, verbose_name="Mã HS")
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Thuế suất (%)")
    
    # Hình ảnh
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Hình ảnh chính")
    
    is_active = models.BooleanField(default=True, verbose_name="Đang kinh doanh")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    
    class Meta:
        verbose_name = "Sản phẩm"
        verbose_name_plural = "Sản phẩm"
        ordering = ['name']
        
    def __str__(self):
        return f"{self.name} ({self.code})"
        
    def profit_margin(self):
        """Tính tỷ suất lợi nhuận"""
        if self.cost_price > 0:
            return ((self.selling_price - self.cost_price) / self.cost_price) * 100
        return 0

class ProductImage(models.Model):
    """Hình ảnh bổ sung của sản phẩm"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/gallery/', verbose_name="Hình ảnh")
    caption = models.CharField(max_length=200, blank=True, verbose_name="Chú thích")
    is_main = models.BooleanField(default=False, verbose_name="Hình ảnh chính")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Hình ảnh sản phẩm"
        verbose_name_plural = "Hình ảnh sản phẩm"
        
    def __str__(self):
        return f"{self.product.name} - {self.caption or 'Image'}"

class ProductSpecification(models.Model):
    """Thông số kỹ thuật sản phẩm"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications')
    name = models.CharField(max_length=100, verbose_name="Tên thông số")
    value = models.CharField(max_length=200, verbose_name="Giá trị")
    unit = models.CharField(max_length=20, blank=True, verbose_name="Đơn vị")
    
    class Meta:
        verbose_name = "Thông số sản phẩm"
        verbose_name_plural = "Thông số sản phẩm"
        unique_together = ['product', 'name']
        
    def __str__(self):
        return f"{self.product.name} - {self.name}: {self.value} {self.unit}"
