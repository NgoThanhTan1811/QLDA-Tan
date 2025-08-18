from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator

class Farmer(models.Model):
    """Model cho thông tin nông dân - nhà cung cấp sản phẩm"""
    FARMER_TYPE_CHOICES = [
        ('individual', 'Cá nhân'),
        ('cooperative', 'Hợp tác xã'),
        ('company', 'Doanh nghiệp'),
    ]
    
    CERTIFICATION_CHOICES = [
        ('organic', 'Hữu cơ'),
        ('vietgap', 'VietGAP'),
        ('globalgap', 'GlobalGAP'),
        ('haccp', 'HACCP'),
        ('iso', 'ISO'),
        ('none', 'Không có'),
    ]
    
    # Thông tin cơ bản
    farmer_code = models.CharField(max_length=20, unique=True, verbose_name="Mã nông dân")
    name = models.CharField(max_length=200, verbose_name="Tên nông dân/Tổ chức")
    farmer_type = models.CharField(max_length=20, choices=FARMER_TYPE_CHOICES, verbose_name="Loại hình")
    
    # Thông tin liên hệ
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Số điện thoại phải có định dạng: '+999999999'. Tối đa 15 chữ số.")
    phone = models.CharField(validators=[phone_regex], max_length=17, verbose_name="Số điện thoại")
    email = models.EmailField(blank=True, verbose_name="Email")
    
    # Địa chỉ và vùng canh tác
    province = models.CharField(max_length=100, verbose_name="Tỉnh/Thành phố")
    district = models.CharField(max_length=100, verbose_name="Quận/Huyện")
    ward = models.CharField(max_length=100, verbose_name="Phường/Xã")
    address = models.TextField(verbose_name="Địa chỉ chi tiết")
    farming_region = models.CharField(max_length=200, verbose_name="Vùng canh tác")
    
    # Thông tin canh tác
    total_farm_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Tổng diện tích canh tác (ha)")
    active_farm_area = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Diện tích đang canh tác (ha)")
    farming_experience = models.IntegerField(validators=[MinValueValidator(0)], default=0, verbose_name="Kinh nghiệm canh tác (năm)")
    main_crops = models.TextField(verbose_name="Cây trồng chính")
    
    # Chứng nhận và chất lượng
    certifications = models.CharField(max_length=20, choices=CERTIFICATION_CHOICES, default='none', verbose_name="Chứng nhận")
    certification_number = models.CharField(max_length=100, blank=True, verbose_name="Số chứng nhận")
    certification_expiry = models.DateField(blank=True, null=True, verbose_name="Ngày hết hạn chứng nhận")
    
    # Thông tin ngân hàng
    bank_name = models.CharField(max_length=100, blank=True, verbose_name="Tên ngân hàng")
    bank_account = models.CharField(max_length=50, blank=True, verbose_name="Số tài khoản")
    account_holder = models.CharField(max_length=100, blank=True, verbose_name="Tên chủ tài khoản")
    
    # Thông tin thuế (nếu có)
    tax_code = models.CharField(max_length=20, blank=True, unique=True, null=True, verbose_name="Mã số thuế")
    
    # Đánh giá và xếp hạng
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0, 
                               validators=[MinValueValidator(0), MaxValueValidator(5)], verbose_name="Đánh giá")
    total_reviews = models.IntegerField(default=0, verbose_name="Tổng số đánh giá")
    
    # Trạng thái
    is_verified = models.BooleanField(default=False, verbose_name="Đã xác minh")
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")
    is_featured = models.BooleanField(default=False, verbose_name="Nông dân nổi bật")
    
    # Thời gian
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    
    class Meta:
        verbose_name = "Nông dân"
        verbose_name_plural = "Nông dân"
        ordering = ['name']
        
    def __str__(self):
        return f"{self.farmer_code} - {self.name}"
        
    def save(self, *args, **kwargs):
        if not self.farmer_code:
            # Tự động tạo mã nông dân
            last_farmer = Farmer.objects.order_by('-id').first()
            if last_farmer and last_farmer.farmer_code:
                try:
                    number = int(last_farmer.farmer_code.split('F')[-1]) + 1
                except:
                    number = 1
            else:
                number = 1
            self.farmer_code = f"F{number:06d}"
        super().save(*args, **kwargs)

class FarmingArea(models.Model):
    """Khu vực canh tác của nông dân"""
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='farming_areas')
    area_name = models.CharField(max_length=200, verbose_name="Tên khu vực")
    area_size = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Diện tích (ha)")
    soil_type = models.CharField(max_length=100, verbose_name="Loại đất")
    water_source = models.CharField(max_length=100, verbose_name="Nguồn nước")
    coordinates = models.CharField(max_length=100, blank=True, verbose_name="Tọa độ GPS")
    description = models.TextField(blank=True, verbose_name="Mô tả")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Khu vực canh tác"
        verbose_name_plural = "Khu vực canh tác"
        
    def __str__(self):
        return f"{self.farmer.name} - {self.area_name}"

class CropProduct(models.Model):
    """Sản phẩm nông nghiệp của nông dân"""
    SEASON_CHOICES = [
        ('spring', 'Xuân'),
        ('summer', 'Hè'),
        ('autumn', 'Thu'),
        ('winter', 'Đông'),
        ('year_round', 'Quanh năm'),
    ]
    
    QUALITY_GRADE_CHOICES = [
        ('premium', 'Cao cấp'),
        ('grade_a', 'Loại A'),
        ('grade_b', 'Loại B'),
        ('standard', 'Tiêu chuẩn'),
    ]
    
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='crop_products')
    farming_area = models.ForeignKey(FarmingArea, on_delete=models.CASCADE, related_name='products')
    
    # Thông tin sản phẩm
    product_name = models.CharField(max_length=200, verbose_name="Tên sản phẩm")
    variety = models.CharField(max_length=100, verbose_name="Giống/Loại")
    
    # Thông tin canh tác
    planting_date = models.DateField(verbose_name="Ngày gieo trồng")
    harvest_season = models.CharField(max_length=20, choices=SEASON_CHOICES, verbose_name="Mùa vụ")
    expected_harvest_date = models.DateField(verbose_name="Ngày dự kiến thu hoạch")
    actual_harvest_date = models.DateField(blank=True, null=True, verbose_name="Ngày thu hoạch thực tế")
    
    # Sản lượng và chất lượng
    estimated_yield = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Sản lượng dự kiến (kg)")
    actual_yield = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Sản lượng thực tế (kg)")
    quality_grade = models.CharField(max_length=20, choices=QUALITY_GRADE_CHOICES, verbose_name="Cấp chất lượng")
    
    # Giá cả
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Giá/kg (VND)")
    min_order_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1, verbose_name="Số lượng đặt hàng tối thiểu")
    
    # Chứng nhận
    is_organic = models.BooleanField(default=False, verbose_name="Sản phẩm hữu cơ")
    has_certificate = models.BooleanField(default=False, verbose_name="Có chứng nhận")
    certificate_type = models.CharField(max_length=100, blank=True, verbose_name="Loại chứng nhận")
    
    # Trạng thái
    is_available = models.BooleanField(default=True, verbose_name="Có sẵn")
    is_featured = models.BooleanField(default=False, verbose_name="Sản phẩm nổi bật")
    
    # Mô tả
    description = models.TextField(blank=True, verbose_name="Mô tả sản phẩm")
    growing_method = models.TextField(blank=True, verbose_name="Phương pháp canh tác")
    harvest_method = models.TextField(blank=True, verbose_name="Phương pháp thu hoạch")
    storage_method = models.TextField(blank=True, verbose_name="Phương pháp bảo quản")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    
    class Meta:
        verbose_name = "Sản phẩm nông nghiệp"
        verbose_name_plural = "Sản phẩm nông nghiệp"
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.farmer.name} - {self.product_name} ({self.variety})"

class FarmerDocument(models.Model):
    """Tài liệu của nông dân"""
    DOCUMENT_TYPE_CHOICES = [
        ('id_card', 'CMND/CCCD'),
        ('business_license', 'Giấy phép kinh doanh'),
        ('land_certificate', 'Giấy chứng nhận quyền sử dụng đất'),
        ('organic_certificate', 'Chứng nhận hữu cơ'),
        ('vietgap_certificate', 'Chứng nhận VietGAP'),
        ('globalgap_certificate', 'Chứng nhận GlobalGAP'),
        ('quality_certificate', 'Chứng nhận chất lượng'),
        ('other', 'Khác'),
    ]
    
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=30, choices=DOCUMENT_TYPE_CHOICES, verbose_name="Loại tài liệu")
    title = models.CharField(max_length=200, verbose_name="Tiêu đề")
    file = models.FileField(upload_to='farmer_documents/', verbose_name="File tài liệu")
    issue_date = models.DateField(blank=True, null=True, verbose_name="Ngày cấp")
    expiry_date = models.DateField(blank=True, null=True, verbose_name="Ngày hết hạn")
    notes = models.TextField(blank=True, verbose_name="Ghi chú")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tải lên")
    
    class Meta:
        verbose_name = "Tài liệu nông dân"
        verbose_name_plural = "Tài liệu nông dân"
        
    def __str__(self):
        return f"{self.farmer.name} - {self.title}"
