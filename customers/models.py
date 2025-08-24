from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.conf import settings

class Customer(models.Model):
    """Model cho thông tin khách hàng - người mua sản phẩm"""
    # Liên kết với User (nếu có tài khoản)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, 
                               related_name='customer_profile', verbose_name="Tài khoản người dùng")
    
    # Thông tin cơ bản
    customer_code = models.CharField(max_length=20, unique=True, verbose_name="Mã khách hàng")
    full_name = models.CharField(max_length=200, verbose_name="Họ và tên")    
    # Thông tin liên hệ
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Số điện thoại phải có định dạng: '+999999999'. Tối đa 15 chữ số.")
    phone = models.CharField(validators=[phone_regex], max_length=17, verbose_name="Số điện thoại")
    email = models.EmailField(verbose_name="Email")
    
    # Địa chỉ
    province = models.CharField(max_length=100, verbose_name="Tỉnh/Thành phố")
    district = models.CharField(max_length=100, verbose_name="Quận/Huyện")
    ward = models.CharField(max_length=100, verbose_name="Phường/Xã")
    address = models.TextField(verbose_name="Địa chỉ chi tiết")
    
    # Trạng thái
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")
    is_verified = models.BooleanField(default=False, verbose_name="Đã xác minh")
        
    # Thời gian
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Ngày sinh")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    
    class Meta:
        verbose_name = "Khách hàng"
        verbose_name_plural = "Khách hàng"
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.customer_code} - {self.full_name}"
        
    def save(self, *args, **kwargs):
        if not self.customer_code:
            # Tự động tạo mã khách hàng
            last_customer = Customer.objects.order_by('-id').first()
            if last_customer and last_customer.customer_code:
                try:
                    number = int(last_customer.customer_code.split('C')[-1]) + 1
                except:
                    number = 1
            else:
                number = 1
            self.customer_code = f"C{number:06d}"
        super().save(*args, **kwargs)
        

class CustomerAddress(models.Model):
    """Địa chỉ giao hàng của khách hàng"""

    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses')
    recipient_name = models.CharField(max_length=100, verbose_name="Tên người nhận")
    phone = models.CharField(max_length=17, verbose_name="Số điện thoại")
    
    province = models.CharField(max_length=100, verbose_name="Tỉnh/Thành phố")
    district = models.CharField(max_length=100, verbose_name="Quận/Huyện")
    ward = models.CharField(max_length=100, verbose_name="Phường/Xã")
    address = models.TextField(verbose_name="Địa chỉ chi tiết")
    
    is_default = models.BooleanField(default=False, verbose_name="Địa chỉ mặc định")
    notes = models.TextField(blank=True, verbose_name="Ghi chú")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Địa chỉ khách hàng"
        verbose_name_plural = "Địa chỉ khách hàng"
        
    def __str__(self):
        return f"{self.customer.full_name} - {self.get_address_type_display()}"
