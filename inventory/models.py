from django.db import models
from django.core.validators import MinValueValidator
from products.models import Product
from farmers.models import Farmer
from customers.models import Customer
from accounts.models import User

class Warehouse(models.Model):
    """Kho hàng"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Tên kho")
    code = models.CharField(max_length=20, unique=True, verbose_name="Mã kho")
    address = models.TextField(verbose_name="Địa chỉ")
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Quản lý kho")
    capacity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Sức chứa (tấn)")
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    
    class Meta:
        verbose_name = "Kho"
        verbose_name_plural = "Kho"
        ordering = ['name']
        
    def __str__(self):
        return f"{self.name} ({self.code})"

class InventoryStock(models.Model):
    """Tồn kho"""
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name="Kho")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Sản phẩm")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Số lượng tồn")
    reserved_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Số lượng đặt trước")
    min_stock_level = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Mức tồn kho tối thiểu")
    max_stock_level = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Mức tồn kho tối đa")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Cập nhật cuối")
    
    class Meta:
        verbose_name = "Tồn kho"
        verbose_name_plural = "Tồn kho"
        unique_together = ['warehouse', 'product']
        
    def __str__(self):
        return f"{self.warehouse.name} - {self.product.name}: {self.quantity}"
        
    @property
    def available_quantity(self):
        """Số lượng có thể bán"""
        return self.quantity - self.reserved_quantity
        
    @property
    def is_low_stock(self):
        """Kiểm tra tồn kho thấp"""
        return self.quantity <= self.min_stock_level

class StockMovement(models.Model):
    """Biến động tồn kho"""
    MOVEMENT_TYPE_CHOICES = [
        ('inbound', 'Nhập kho'),
        ('outbound', 'Xuất kho'),
        ('transfer', 'Chuyển kho'),
        ('adjustment', 'Điều chỉnh'),
        ('damaged', 'Hàng hỏng'),
        ('expired', 'Hàng hết hạn'),
    ]
    
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name="Kho")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Sản phẩm")
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPE_CHOICES, verbose_name="Loại biến động")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Số lượng")
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name="Đơn giá")
    reference_type = models.CharField(max_length=50, blank=True, verbose_name="Loại tham chiếu")
    reference_id = models.PositiveIntegerField(blank=True, null=True, verbose_name="ID tham chiếu")
    notes = models.TextField(blank=True, verbose_name="Ghi chú")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Người tạo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    
    class Meta:
        verbose_name = "Biến động tồn kho"
        verbose_name_plural = "Biến động tồn kho"
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.warehouse.name} - {self.product.name}: {self.get_movement_type_display()} {self.quantity}"

class StockTaking(models.Model):
    """Kiểm kê tồn kho"""
    STATUS_CHOICES = [
        ('draft', 'Nháp'),
        ('in_progress', 'Đang kiểm kê'),
        ('completed', 'Hoàn thành'),
        ('cancelled', 'Hủy'),
    ]
    
    code = models.CharField(max_length=20, unique=True, verbose_name="Mã kiểm kê")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, verbose_name="Kho")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="Trạng thái")
    start_date = models.DateTimeField(verbose_name="Ngày bắt đầu")
    end_date = models.DateTimeField(blank=True, null=True, verbose_name="Ngày kết thúc")
    notes = models.TextField(blank=True, verbose_name="Ghi chú")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Người tạo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    
    class Meta:
        verbose_name = "Kiểm kê"
        verbose_name_plural = "Kiểm kê"
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Kiểm kê {self.code} - {self.warehouse.name}"

class StockTakingDetail(models.Model):
    """Chi tiết kiểm kê"""
    stock_taking = models.ForeignKey(StockTaking, on_delete=models.CASCADE, related_name='details')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Sản phẩm")
    system_quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Số lượng hệ thống")
    actual_quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Số lượng thực tế")
    variance = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Chênh lệch")
    notes = models.TextField(blank=True, verbose_name="Ghi chú")
    
    class Meta:
        verbose_name = "Chi tiết kiểm kê"
        verbose_name_plural = "Chi tiết kiểm kê"
        unique_together = ['stock_taking', 'product']
        
    def save(self, *args, **kwargs):
        self.variance = self.actual_quantity - self.system_quantity
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.stock_taking.code} - {self.product.name}"
