from django.db import models
from django.core.validators import MinValueValidator
from orders.models import Order
from farmers.models import Farmer
from customers.models import Customer
from accounts.models import User

class Payment(models.Model):
    """Thanh toán"""
    PAYMENT_TYPE_CHOICES = [
        ('inbound', 'Thu tiền (Khách trả)'),
        ('outbound', 'Chi tiền (Trả nhà cung cấp)'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Tiền mặt'),
        ('bank_transfer', 'Chuyển khoản'),
        ('check', 'Séc'),
        ('credit_card', 'Thẻ tín dụng'),
        ('letter_of_credit', 'Thư tín dụng (L/C)'),
        ('other', 'Khác'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Chờ xử lý'),
        ('completed', 'Hoàn thành'),
        ('failed', 'Thất bại'),
        ('cancelled', 'Đã hủy'),
    ]
    
    payment_code = models.CharField(max_length=50, unique=True, verbose_name="Mã thanh toán")
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES, verbose_name="Loại thanh toán")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments', verbose_name="Đơn hàng")
    
    # Thay thế Company bằng Farmer hoặc Customer dựa trên loại thanh toán
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, null=True, blank=True, 
                              verbose_name="Nông dân", help_text="Thanh toán cho nông dân")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True,
                               verbose_name="Khách hàng", help_text="Thanh toán từ khách hàng")
    
    amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Số tiền")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name="Phương thức thanh toán")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Trạng thái")
    
    # Ngày tháng
    payment_date = models.DateField(verbose_name="Ngày thanh toán")
    due_date = models.DateField(blank=True, null=True, verbose_name="Ngày đến hạn")
    
    # Thông tin ngân hàng
    bank_name = models.CharField(max_length=100, blank=True, verbose_name="Tên ngân hàng")
    bank_account = models.CharField(max_length=50, blank=True, verbose_name="Số tài khoản")
    transaction_reference = models.CharField(max_length=100, blank=True, verbose_name="Mã giao dịch")
    
    # Thông tin khác
    notes = models.TextField(blank=True, verbose_name="Ghi chú")
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4, default=1, verbose_name="Tỷ giá")
    currency = models.CharField(max_length=3, default='VND', verbose_name="Tiền tệ")
    
    # Thông tin người tạo
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Người tạo")
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='approved_payments', blank=True, verbose_name="Người duyệt")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    
    class Meta:
        verbose_name = "Thanh toán"
        verbose_name_plural = "Thanh toán"
        ordering = ['-created_at']
        
    def __str__(self):
        partner_name = ""
        if self.farmer:
            partner_name = self.farmer.name
        elif self.customer:
            partner_name = self.customer.full_name
        else:
            partner_name = "Unknown"
        return f"{self.payment_code} - {partner_name}: {self.amount:,} VND"
        
    def save(self, *args, **kwargs):
        if not self.payment_code:
            # Tự động tạo mã thanh toán
            prefix = 'PAY'
            last_payment = Payment.objects.order_by('-id').first()
            if last_payment:
                number = int(last_payment.payment_code.split('-')[-1]) + 1
            else:
                number = 1
            self.payment_code = f"{prefix}-{number:06d}"
        super().save(*args, **kwargs)

class PaymentDocument(models.Model):
    """Tài liệu thanh toán"""
    DOCUMENT_TYPE_CHOICES = [
        ('receipt', 'Phiếu thu'),
        ('payment_voucher', 'Phiếu chi'),
        ('bank_statement', 'Sao kê ngân hàng'),
        ('invoice', 'Hóa đơn'),
        ('contract', 'Hợp đồng'),
        ('other', 'Khác'),
    ]
    
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES, verbose_name="Loại tài liệu")
    title = models.CharField(max_length=200, verbose_name="Tiêu đề")
    file = models.FileField(upload_to='payment_documents/', verbose_name="File")
    notes = models.TextField(blank=True, verbose_name="Ghi chú")
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Người tải lên")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tải lên")
    
    class Meta:
        verbose_name = "Tài liệu thanh toán"
        verbose_name_plural = "Tài liệu thanh toán"
        
    def __str__(self):
        return f"{self.payment.payment_code} - {self.title}"

class PaymentSchedule(models.Model):
    """Lịch thanh toán"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payment_schedules', verbose_name="Đơn hàng")
    sequence = models.PositiveIntegerField(verbose_name="Số thứ tự")
    amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Số tiền")
    due_date = models.DateField(verbose_name="Ngày đến hạn")
    description = models.CharField(max_length=200, verbose_name="Mô tả")
    is_paid = models.BooleanField(default=False, verbose_name="Đã thanh toán")
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Thanh toán")
    notes = models.TextField(blank=True, verbose_name="Ghi chú")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    
    class Meta:
        verbose_name = "Lịch thanh toán"
        verbose_name_plural = "Lịch thanh toán"
        unique_together = ['order', 'sequence']
        ordering = ['order', 'sequence']
        
    def __str__(self):
        return f"{self.order.order_number} - Đợt {self.sequence}: {self.amount:,}"

class ExchangeRate(models.Model):
    """Tỷ giá hối đoái"""
    from_currency = models.CharField(max_length=3, verbose_name="Từ tiền tệ")
    to_currency = models.CharField(max_length=3, verbose_name="Sang tiền tệ")
    rate = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="Tỷ giá")
    effective_date = models.DateField(verbose_name="Ngày hiệu lực")
    notes = models.TextField(blank=True, verbose_name="Ghi chú")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Người tạo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    
    class Meta:
        verbose_name = "Tỷ giá"
        verbose_name_plural = "Tỷ giá"
        unique_together = ['from_currency', 'to_currency', 'effective_date']
        ordering = ['-effective_date']
        
    def __str__(self):
        return f"{self.from_currency}/{self.to_currency}: {self.rate} ({self.effective_date})"
