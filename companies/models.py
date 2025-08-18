from django.db import models

class Company(models.Model):
    """Model cho thông tin công ty"""
    COMPANY_TYPE_CHOICES = [
        ('our_company', 'Công ty chúng tôi'),
        ('supplier', 'Nhà cung cấp'),
        ('customer', 'Khách hàng'),
        ('partner', 'Đối tác'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Tên công ty")
    company_type = models.CharField(max_length=20, choices=COMPANY_TYPE_CHOICES, verbose_name="Loại công ty")
    tax_code = models.CharField(max_length=20, unique=True, verbose_name="Mã số thuế")
    address = models.TextField(verbose_name="Địa chỉ")
    phone = models.CharField(max_length=15, blank=True, verbose_name="Số điện thoại")
    email = models.EmailField(blank=True, verbose_name="Email")
    website = models.URLField(blank=True, verbose_name="Website")
    
    # Thông tin ngân hàng
    bank_name = models.CharField(max_length=100, blank=True, verbose_name="Tên ngân hàng")
    bank_account = models.CharField(max_length=50, blank=True, verbose_name="Số tài khoản")
    
    # Thông tin liên hệ
    contact_person = models.CharField(max_length=100, blank=True, verbose_name="Người liên hệ")
    contact_phone = models.CharField(max_length=15, blank=True, verbose_name="SĐT người liên hệ")
    contact_email = models.EmailField(blank=True, verbose_name="Email người liên hệ")
    
    # Thông tin xuất nhập khẩu
    import_license = models.CharField(max_length=50, blank=True, verbose_name="Giấy phép nhập khẩu")
    export_license = models.CharField(max_length=50, blank=True, verbose_name="Giấy phép xuất khẩu")
    
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    
    class Meta:
        verbose_name = "Công ty"
        verbose_name_plural = "Công ty"
        ordering = ['name']
        
    def __str__(self):
        return f"{self.name} ({self.get_company_type_display()})"

class CompanyDocument(models.Model):
    """Tài liệu của công ty"""
    DOCUMENT_TYPE_CHOICES = [
        ('business_license', 'Giấy phép kinh doanh'),
        ('tax_certificate', 'Giấy chứng nhận thuế'),
        ('import_license', 'Giấy phép nhập khẩu'),
        ('export_license', 'Giấy phép xuất khẩu'),
        ('other', 'Khác'),
    ]
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES, verbose_name="Loại tài liệu")
    title = models.CharField(max_length=200, verbose_name="Tiêu đề")
    file = models.FileField(upload_to='company_documents/', verbose_name="File tài liệu")
    expiry_date = models.DateField(blank=True, null=True, verbose_name="Ngày hết hạn")
    notes = models.TextField(blank=True, verbose_name="Ghi chú")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tải lên")
    
    class Meta:
        verbose_name = "Tài liệu công ty"
        verbose_name_plural = "Tài liệu công ty"
        
    def __str__(self):
        return f"{self.company.name} - {self.title}"

class UpdateCompany(models.Model):
    """Model cho cập nhật thông tin công ty"""
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='updates')
    title = models.CharField(max_length=200, verbose_name="Tiêu đề cập nhật")
    content = models.TextField(verbose_name="Nội dung cập nhật")
    update_date = models.DateTimeField(auto_now_add=True, verbose_name="Ngày cập nhật")
    class Meta:
        verbose_name = "Cập nhật công ty"
        verbose_name_plural = "Cập nhật công ty"
        ordering = ['-update_date']
    def __str__(self):
        return f"{self.company.name} - {self.title} ({self.update_date.strftime('%Y-%m-%d')})"
