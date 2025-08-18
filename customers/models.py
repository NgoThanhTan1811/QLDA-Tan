from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.conf import settings

class Customer(models.Model):
    """Model cho thông tin khách hàng - người mua sản phẩm"""
    CUSTOMER_TYPE_CHOICES = [
        ('individual', 'Cá nhân'),
        ('restaurant', 'Nhà hàng'),
        ('supermarket', 'Siêu thị'),
        ('distributor', 'Nhà phân phối'),
        ('retailer', 'Nhà bán lẻ'),
        ('exporter', 'Xuất khẩu'),
    ]
    
    MEMBERSHIP_CHOICES = [
        ('bronze', 'Đồng'),
        ('silver', 'Bạc'),
        ('gold', 'Vàng'),
        ('platinum', 'Bạch kim'),
        ('diamond', 'Kim cương'),
    ]
    
    # Liên kết với User (nếu có tài khoản)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, 
                               related_name='customer_profile', verbose_name="Tài khoản người dùng")
    
    # Thông tin cơ bản
    customer_code = models.CharField(max_length=20, unique=True, verbose_name="Mã khách hàng")
    full_name = models.CharField(max_length=200, verbose_name="Họ và tên")
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPE_CHOICES, verbose_name="Loại khách hàng")
    
    # Thông tin liên hệ
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Số điện thoại phải có định dạng: '+999999999'. Tối đa 15 chữ số.")
    phone = models.CharField(validators=[phone_regex], max_length=17, verbose_name="Số điện thoại")
    email = models.EmailField(verbose_name="Email")
    
    # Địa chỉ
    province = models.CharField(max_length=100, verbose_name="Tỉnh/Thành phố")
    district = models.CharField(max_length=100, verbose_name="Quận/Huyện")
    ward = models.CharField(max_length=100, verbose_name="Phường/Xã")
    address = models.TextField(verbose_name="Địa chỉ chi tiết")
    
    # Thông tin doanh nghiệp (nếu có)
    company_name = models.CharField(max_length=200, blank=True, verbose_name="Tên công ty")
    tax_code = models.CharField(max_length=20, blank=True, unique=True, null=True, verbose_name="Mã số thuế")
    business_license = models.CharField(max_length=50, blank=True, verbose_name="Giấy phép kinh doanh")
    
    # Thông tin thanh toán
    bank_name = models.CharField(max_length=100, blank=True, verbose_name="Tên ngân hàng")
    bank_account = models.CharField(max_length=50, blank=True, verbose_name="Số tài khoản")
    account_holder = models.CharField(max_length=100, blank=True, verbose_name="Tên chủ tài khoản")
    
    # Thành viên và ưu đãi
    membership_level = models.CharField(max_length=10, choices=MEMBERSHIP_CHOICES, default='bronze', verbose_name="Cấp thành viên")
    points = models.IntegerField(default=0, verbose_name="Điểm tích lũy")
    credit_limit = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Hạn mức tín dụng")
    
    # Sở thích mua sắm
    preferred_products = models.TextField(blank=True, verbose_name="Sản phẩm ưa thích")
    preferred_payment_method = models.CharField(max_length=50, blank=True, verbose_name="Phương thức thanh toán ưa thích")
    preferred_delivery_time = models.CharField(max_length=100, blank=True, verbose_name="Thời gian giao hàng ưa thích")
    
    # Thống kê mua sắm
    total_orders = models.IntegerField(default=0, verbose_name="Tổng số đơn hàng")
    total_spent = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Tổng chi tiêu")
    average_order_value = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Giá trị đơn hàng trung bình")
    
    # Đánh giá khách hàng
    customer_rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0,
                                        validators=[MinValueValidator(0), MaxValueValidator(5)], 
                                        verbose_name="Đánh giá khách hàng")
    
    # Trạng thái
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")
    is_verified = models.BooleanField(default=False, verbose_name="Đã xác minh")
    is_vip = models.BooleanField(default=False, verbose_name="Khách hàng VIP")
    
    # Thời gian
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Ngày sinh")
    first_order_date = models.DateTimeField(blank=True, null=True, verbose_name="Ngày đặt hàng đầu tiên")
    last_order_date = models.DateTimeField(blank=True, null=True, verbose_name="Ngày đặt hàng cuối")
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
        
    def update_membership_level(self):
        """Cập nhật cấp thành viên dựa trên tổng chi tiêu"""
        if self.total_spent >= 100000000:  # 100 triệu
            self.membership_level = 'diamond'
        elif self.total_spent >= 50000000:  # 50 triệu
            self.membership_level = 'platinum'
        elif self.total_spent >= 20000000:  # 20 triệu
            self.membership_level = 'gold'
        elif self.total_spent >= 5000000:   # 5 triệu
            self.membership_level = 'silver'
        else:
            self.membership_level = 'bronze'
        self.save()

class CustomerAddress(models.Model):
    """Địa chỉ giao hàng của khách hàng"""
    ADDRESS_TYPE_CHOICES = [
        ('home', 'Nhà riêng'),
        ('office', 'Văn phòng'),
        ('warehouse', 'Kho hàng'),
        ('other', 'Khác'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses')
    address_type = models.CharField(max_length=20, choices=ADDRESS_TYPE_CHOICES, verbose_name="Loại địa chỉ")
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

class CustomerReview(models.Model):
    """Đánh giá của khách hàng về nông dân/sản phẩm"""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reviews')
    farmer = models.ForeignKey('farmers.Farmer', on_delete=models.CASCADE, related_name='customer_reviews')
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, blank=True, null=True, related_name='reviews')
    
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="Đánh giá (1-5 sao)")
    title = models.CharField(max_length=200, verbose_name="Tiêu đề đánh giá")
    content = models.TextField(verbose_name="Nội dung đánh giá")
    
    # Đánh giá chi tiết
    product_quality = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="Chất lượng sản phẩm")
    delivery_time = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="Thời gian giao hàng")
    service_quality = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="Chất lượng dịch vụ")
    
    is_verified = models.BooleanField(default=False, verbose_name="Đánh giá đã xác thực")
    is_featured = models.BooleanField(default=False, verbose_name="Đánh giá nổi bật")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    
    class Meta:
        verbose_name = "Đánh giá khách hàng"
        verbose_name_plural = "Đánh giá khách hàng"
        ordering = ['-created_at']
        unique_together = ['customer', 'farmer', 'order']
        
    def __str__(self):
        return f"{self.customer.full_name} đánh giá {self.farmer.name} - {self.rating} sao"

class CustomerWishlist(models.Model):
    """Danh sách yêu thích của khách hàng"""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='wishlist')
    farmer = models.ForeignKey('farmers.Farmer', on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey('farmers.CropProduct', on_delete=models.CASCADE, blank=True, null=True)
    
    notes = models.TextField(blank=True, verbose_name="Ghi chú")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Danh sách yêu thích"
        verbose_name_plural = "Danh sách yêu thích"
        
    def __str__(self):
        if self.product:
            return f"{self.customer.full_name} - {self.product.product_name}"
        return f"{self.customer.full_name} - {self.farmer.name}"

class CustomerDocument(models.Model):
    """Tài liệu của khách hàng"""
    DOCUMENT_TYPE_CHOICES = [
        ('id_card', 'CMND/CCCD'),
        ('business_license', 'Giấy phép kinh doanh'),
        ('tax_certificate', 'Giấy chứng nhận thuế'),
        ('contract', 'Hợp đồng'),
        ('other', 'Khác'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES, verbose_name="Loại tài liệu")
    title = models.CharField(max_length=200, verbose_name="Tiêu đề")
    file = models.FileField(upload_to='customer_documents/', verbose_name="File tài liệu")
    issue_date = models.DateField(blank=True, null=True, verbose_name="Ngày cấp")
    expiry_date = models.DateField(blank=True, null=True, verbose_name="Ngày hết hạn")
    notes = models.TextField(blank=True, verbose_name="Ghi chú")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tải lên")
    
    class Meta:
        verbose_name = "Tài liệu khách hàng"
        verbose_name_plural = "Tài liệu khách hàng"
        
    def __str__(self):
        return f"{self.customer.full_name} - {self.title}"
