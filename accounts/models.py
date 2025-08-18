from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Custom User model với các trường bổ sung"""
    ROLE_CHOICES = [
        ('admin', 'Quản trị viên'),
        ('manager', 'Quản lý'),
        ('staff', 'Nhân viên'),
        ('accountant', 'Kế toán'),
    ]
    
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="Số điện thoại")
    address = models.TextField(blank=True, null=True, verbose_name="Địa chỉ")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='staff', verbose_name="Vai trò")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Ảnh đại diện")
    is_active_employee = models.BooleanField(default=True, verbose_name="Đang làm việc")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    
    class Meta:
        verbose_name = "Người dùng"
        verbose_name_plural = "Người dùng"
        
    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"
        
    def get_role_display_vietnamese(self):
        """Hiển thị vai trò bằng tiếng Việt"""
        return dict(self.ROLE_CHOICES).get(self.role, self.role)

class UserProfile(models.Model):
    """Thông tin mở rộng của User"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    employee_id = models.CharField(max_length=10, unique=True, verbose_name="Mã nhân viên")
    department = models.CharField(max_length=100, blank=True, verbose_name="Phòng ban")
    position = models.CharField(max_length=100, blank=True, verbose_name="Chức vụ")
    hire_date = models.DateField(blank=True, null=True, verbose_name="Ngày vào làm")
    salary = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name="Lương")
    
    class Meta:
        verbose_name = "Hồ sơ nhân viên"
        verbose_name_plural = "Hồ sơ nhân viên"
        
    def __str__(self):
        return f"Profile of {self.user.get_full_name()}"
