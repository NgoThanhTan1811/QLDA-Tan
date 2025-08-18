from django.db import models
from orders.models import Order
from accounts.models import User

class ImportExportDocument(models.Model):
    """Tài liệu xuất nhập khẩu"""
    DOCUMENT_TYPE_CHOICES = [
        ('customs_declaration', 'Tờ khai hải quan'),
        ('commercial_invoice', 'Hóa đơn thương mại'),
        ('packing_list', 'Danh sách đóng gói'),
        ('bill_of_lading', 'Vận đơn'),
        ('certificate_of_origin', 'Giấy chứng nhận xuất xứ (CO)'),
        ('quality_certificate', 'Giấy chứng nhận chất lượng (CQ)'),
        ('phytosanitary_certificate', 'Giấy chứng nhận kiểm dịch thực vật'),
        ('insurance_certificate', 'Giấy chứng nhận bảo hiểm'),
        ('letter_of_credit', 'Thư tín dụng'),
        ('inspection_certificate', 'Giấy chứng nhận kiểm tra'),
        ('other', 'Khác'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Nháp'),
        ('submitted', 'Đã nộp'),
        ('approved', 'Đã duyệt'),
        ('rejected', 'Bị từ chối'),
        ('expired', 'Hết hạn'),
    ]
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='import_export_documents', verbose_name="Đơn hàng")
    document_type = models.CharField(max_length=30, choices=DOCUMENT_TYPE_CHOICES, verbose_name="Loại tài liệu")
    document_number = models.CharField(max_length=100, verbose_name="Số tài liệu")
    title = models.CharField(max_length=200, verbose_name="Tiêu đề")
    
    # Thông tin tài liệu
    issue_date = models.DateField(verbose_name="Ngày phát hành")
    expiry_date = models.DateField(blank=True, null=True, verbose_name="Ngày hết hạn")
    issuing_authority = models.CharField(max_length=200, blank=True, verbose_name="Cơ quan cấp")
    
    # Trạng thái và xử lý
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="Trạng thái")
    submission_date = models.DateField(blank=True, null=True, verbose_name="Ngày nộp")
    approval_date = models.DateField(blank=True, null=True, verbose_name="Ngày duyệt")
    
    # File và ghi chú
    file = models.FileField(upload_to='import_export_documents/', verbose_name="File tài liệu")
    notes = models.TextField(blank=True, verbose_name="Ghi chú")
    
    # Thông tin người tạo/cập nhật
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_ie_documents', verbose_name="Người tạo")
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='approved_ie_documents', blank=True, verbose_name="Người duyệt")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    
    class Meta:
        verbose_name = "Tài liệu xuất nhập khẩu"
        verbose_name_plural = "Tài liệu xuất nhập khẩu"
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.order.order_number} - {self.get_document_type_display()}: {self.document_number}"

class CustomsDeclaration(models.Model):
    """Tờ khai hải quan"""
    DECLARATION_TYPE_CHOICES = [
        ('import', 'Nhập khẩu'),
        ('export', 'Xuất khẩu'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Nháp'),
        ('submitted', 'Đã nộp'),
        ('processing', 'Đang xử lý'),
        ('cleared', 'Đã thông quan'),
        ('rejected', 'Bị từ chối'),
    ]
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='customs_declaration', verbose_name="Đơn hàng")
    declaration_number = models.CharField(max_length=50, unique=True, verbose_name="Số tờ khai")
    declaration_type = models.CharField(max_length=20, choices=DECLARATION_TYPE_CHOICES, verbose_name="Loại tờ khai")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="Trạng thái")
    
    # Thông tin hải quan
    customs_office = models.CharField(max_length=200, verbose_name="Cơ quan hải quan")
    port_of_entry = models.CharField(max_length=200, verbose_name="Cửa khẩu")
    
    # Ngày tháng
    declaration_date = models.DateField(verbose_name="Ngày khai báo")
    submission_date = models.DateField(blank=True, null=True, verbose_name="Ngày nộp")
    clearance_date = models.DateField(blank=True, null=True, verbose_name="Ngày thông quan")
    
    # Thông tin tài chính
    declared_value = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Giá trị khai báo")
    currency = models.CharField(max_length=3, default='VND', verbose_name="Tiền tệ")
    customs_duty = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Thuế quan")
    vat_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Thuế VAT")
    other_fees = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Phí khác")
    total_tax = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Tổng thuế phí")
    
    # Thông tin khác
    notes = models.TextField(blank=True, verbose_name="Ghi chú")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Người tạo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    
    class Meta:
        verbose_name = "Tờ khai hải quan"
        verbose_name_plural = "Tờ khai hải quan"
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Tờ khai {self.declaration_number} - {self.order.order_number}"
        
    def save(self, *args, **kwargs):
        if not self.declaration_number:
            # Tự động tạo số tờ khai
            prefix = 'TK'
            last_declaration = CustomsDeclaration.objects.order_by('-id').first()
            if last_declaration:
                number = int(last_declaration.declaration_number.split('-')[-1]) + 1
            else:
                number = 1
            self.declaration_number = f"{prefix}-{number:06d}"
        
        self.total_tax = self.customs_duty + self.vat_amount + self.other_fees
        super().save(*args, **kwargs)

class ShippingDocument(models.Model):
    """Tài liệu vận chuyển"""
    DOCUMENT_TYPE_CHOICES = [
        ('bill_of_lading', 'Vận đơn (B/L)'),
        ('airway_bill', 'Vận đơn hàng không (AWB)'),
        ('trucking_bill', 'Vận đơn đường bộ'),
        ('container_list', 'Danh sách container'),
        ('delivery_order', 'Lệnh giao hàng'),
    ]
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='shipping_documents', verbose_name="Đơn hàng")
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES, verbose_name="Loại tài liệu")
    document_number = models.CharField(max_length=100, verbose_name="Số tài liệu")
    
    # Thông tin vận chuyển
    carrier_name = models.CharField(max_length=200, verbose_name="Hãng vận tải")
    vessel_name = models.CharField(max_length=200, blank=True, verbose_name="Tên tàu/máy bay")
    voyage_number = models.CharField(max_length=50, blank=True, verbose_name="Số chuyến")
    
    # Địa điểm
    port_of_loading = models.CharField(max_length=200, verbose_name="Cảng xếp hàng")
    port_of_discharge = models.CharField(max_length=200, verbose_name="Cảng dỡ hàng")
    place_of_delivery = models.CharField(max_length=200, blank=True, verbose_name="Nơi giao hàng")
    
    # Ngày tháng
    issue_date = models.DateField(verbose_name="Ngày phát hành")
    etd = models.DateField(blank=True, null=True, verbose_name="Ngày khởi hành dự kiến")
    eta = models.DateField(blank=True, null=True, verbose_name="Ngày đến dự kiến")
    
    # File và ghi chú
    file = models.FileField(upload_to='shipping_documents/', verbose_name="File tài liệu")
    notes = models.TextField(blank=True, verbose_name="Ghi chú")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Người tạo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    
    class Meta:
        verbose_name = "Tài liệu vận chuyển"
        verbose_name_plural = "Tài liệu vận chuyển"
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.order.order_number} - {self.get_document_type_display()}: {self.document_number}"
