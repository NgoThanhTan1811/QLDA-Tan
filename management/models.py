from django.db import models
from django.core.validators import RegexValidator, EmailValidator
from django.urls import reverse
from PIL import Image


class Employee(models.Model):
    """Model cho nhân viên"""
    GENDER_CHOICES = [
        ('male', 'Nam'),
        ('female', 'Nữ'),
        ('other', 'Khác'),
    ]
    
    DEPARTMENT_CHOICES = [
        ('sales', 'Kinh doanh'),
        ('warehouse', 'Kho'),
        ('admin', 'Hành chính'),
        ('finance', 'Tài chính'),
        ('it', 'Công nghệ thông tin'),
        ('hr', 'Nhân sự'),
    ]
    
    POSITION_CHOICES = [
        ('manager', 'Quản lý'),
        ('supervisor', 'Giám sát'),
        ('staff', 'Nhân viên'),
        ('intern', 'Thực tập sinh'),
    ]
    
    EDUCATION_CHOICES = [
        ('high_school', 'Trung học phổ thông'),
        ('college', 'Cao đẳng'),
        ('university', 'Đại học'),
        ('master', 'Thạc sĩ'),
        ('doctor', 'Tiến sĩ'),
    ]
    
    MARITAL_CHOICES = [
        ('single', 'Độc thân'),
        ('married', 'Đã kết hôn'),
        ('divorced', 'Đã ly hôn'),
    ]
    
    # Basic Info
    employee_id = models.CharField(max_length=20, unique=True, verbose_name="Mã nhân viên")
    first_name = models.CharField(max_length=50, verbose_name="Họ")
    last_name = models.CharField(max_length=50, verbose_name="Tên")
    nickname = models.CharField(max_length=50, blank=True, verbose_name="Tên thường gọi")
    full_name = models.CharField(max_length=100, verbose_name="Họ tên đầy đủ", editable=False)
    
    # Personal Info
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, verbose_name="Giới tính")
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Ngày sinh")
    national_id = models.CharField(max_length=20, blank=True, verbose_name="CMND/CCCD")
    avatar = models.ImageField(upload_to='employees/avatars/', blank=True, verbose_name="Ảnh đại diện")
    
    # Contact Info
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Số điện thoại")
    address = models.TextField(blank=True, verbose_name="Địa chỉ")
    emergency_contact_name = models.CharField(max_length=100, blank=True, verbose_name="Người liên hệ khẩn cấp")
    emergency_contact_phone = models.CharField(max_length=20, blank=True, verbose_name="SĐT người liên hệ khẩn cấp")
    
    # Work Info
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES, verbose_name="Phòng ban")
    position = models.CharField(max_length=20, choices=POSITION_CHOICES, verbose_name="Chức vụ")
    hire_date = models.DateField(verbose_name="Ngày vào làm")
    salary = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name="Lương cơ bản")
    job_description = models.TextField(blank=True, verbose_name="Mô tả công việc")
    
    # Additional Info
    education_level = models.CharField(max_length=20, choices=EDUCATION_CHOICES, blank=True, verbose_name="Trình độ học vấn")
    marital_status = models.CharField(max_length=20, choices=MARITAL_CHOICES, blank=True, verbose_name="Tình trạng hôn nhân")
    bank_account = models.CharField(max_length=50, blank=True, verbose_name="Số tài khoản")
    bank_name = models.CharField(max_length=100, blank=True, verbose_name="Tên ngân hàng")
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name="Đang làm việc")
    notes = models.TextField(blank=True, verbose_name="Ghi chú")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    
    class Meta:
        verbose_name = "Nhân viên"
        verbose_name_plural = "Nhân viên"
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        self.full_name = f"{self.first_name} {self.last_name}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.employee_id} - {self.full_name}"


class Customer(models.Model):
    """Model cho khách hàng"""
    CUSTOMER_TYPE_CHOICES = [
        ('individual', 'Cá nhân'),
        ('business', 'Doanh nghiệp'),
        ('government', 'Cơ quan nhà nước'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Thấp'),
        ('medium', 'Trung bình'),
        ('high', 'Cao'),
    ]
    
    # Basic Info
    customer_code = models.CharField(max_length=20, unique=True, verbose_name="Mã khách hàng")
    name = models.CharField(max_length=200, verbose_name="Tên khách hàng")
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPE_CHOICES, verbose_name="Loại khách hàng")
    avatar = models.ImageField(upload_to='customers/avatars/', blank=True, verbose_name="Ảnh đại diện")
    
    # Contact Info
    email = models.EmailField(blank=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Số điện thoại")
    address = models.TextField(blank=True, verbose_name="Địa chỉ")
    website = models.URLField(blank=True, verbose_name="Website")
    
    # Business Info (for business customers)
    tax_code = models.CharField(max_length=20, blank=True, verbose_name="Mã số thuế")
    business_license = models.CharField(max_length=50, blank=True, verbose_name="Giấy phép kinh doanh")
    representative_name = models.CharField(max_length=100, blank=True, verbose_name="Người đại diện")
    representative_title = models.CharField(max_length=100, blank=True, verbose_name="Chức vụ người đại diện")
    
    # Additional Info
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium', verbose_name="Mức ưu tiên")
    is_vip = models.BooleanField(default=False, verbose_name="Khách hàng VIP")
    credit_limit = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Hạn mức tín dụng")
    payment_terms = models.CharField(max_length=100, blank=True, verbose_name="Điều kiện thanh toán")
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name="Hoạt động")
    notes = models.TextField(blank=True, verbose_name="Ghi chú")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    
    class Meta:
        verbose_name = "Khách hàng"
        verbose_name_plural = "Khách hàng"
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        # Auto generate customer code if not provided
        if not self.customer_code:
            last_customer = Customer.objects.order_by('-id').first()
            if last_customer:
                last_id = int(last_customer.customer_code.replace('KH', ''))
                self.customer_code = f"KH{last_id + 1:05d}"
            else:
                self.customer_code = "KH00001"
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.customer_code} - {self.name}"
