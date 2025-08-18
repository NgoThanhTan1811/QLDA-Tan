from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from accounts.models import User
import json

class ActivityLog(models.Model):
    """Nhật ký hoạt động"""
    ACTION_CHOICES = [
        ('create', 'Tạo mới'),
        ('update', 'Cập nhật'),
        ('delete', 'Xóa'),
        ('view', 'Xem'),
        ('login', 'Đăng nhập'),
        ('logout', 'Đăng xuất'),
        ('export', 'Xuất dữ liệu'),
        ('import', 'Nhập dữ liệu'),
        ('approve', 'Duyệt'),
        ('reject', 'Từ chối'),
        ('cancel', 'Hủy'),
        ('restore', 'Khôi phục'),
        ('other', 'Khác'),
    ]
    
    SEVERITY_CHOICES = [
        ('low', 'Thấp'),
        ('medium', 'Trung bình'),
        ('high', 'Cao'),
        ('critical', 'Nghiêm trọng'),
    ]
    
    # Thông tin cơ bản
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Người thực hiện")
    action = models.CharField(max_length=20, choices=ACTION_CHOICES, verbose_name="Hành động")
    description = models.TextField(verbose_name="Mô tả")
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='low', verbose_name="Mức độ")
    
    # Đối tượng bị tác động (Generic Foreign Key)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Thông tin kỹ thuật
    ip_address = models.GenericIPAddressField(verbose_name="Địa chỉ IP")
    user_agent = models.TextField(blank=True, verbose_name="User Agent")
    session_key = models.CharField(max_length=40, blank=True, verbose_name="Session Key")
    
    # Dữ liệu thay đổi (JSON)
    old_values = models.JSONField(default=dict, blank=True, verbose_name="Giá trị cũ")
    new_values = models.JSONField(default=dict, blank=True, verbose_name="Giá trị mới")
    extra_data = models.JSONField(default=dict, blank=True, verbose_name="Dữ liệu bổ sung")
    
    # Thời gian
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Thời gian")
    
    class Meta:
        verbose_name = "Nhật ký hoạt động"
        verbose_name_plural = "Nhật ký hoạt động"
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['action', 'timestamp']),
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['ip_address', 'timestamp']),
        ]
        
    def __str__(self):
        user_name = self.user.get_full_name() if self.user else "Hệ thống"
        return f"{user_name} - {self.get_action_display()}: {self.description}"
        
    def get_changes_summary(self):
        """Tóm tắt thay đổi"""
        if not self.old_values and not self.new_values:
            return "Không có thay đổi"
            
        changes = []
        all_fields = set(self.old_values.keys()) | set(self.new_values.keys())
        
        for field in all_fields:
            old_value = self.old_values.get(field, "")
            new_value = self.new_values.get(field, "")
            if old_value != new_value:
                changes.append(f"{field}: '{old_value}' → '{new_value}'")
        
        return "; ".join(changes) if changes else "Không có thay đổi"

class LoginHistory(models.Model):
    """Lịch sử đăng nhập"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_history', verbose_name="Người dùng")
    login_time = models.DateTimeField(auto_now_add=True, verbose_name="Thời gian đăng nhập")
    logout_time = models.DateTimeField(null=True, blank=True, verbose_name="Thời gian đăng xuất")
    ip_address = models.GenericIPAddressField(verbose_name="Địa chỉ IP")
    user_agent = models.TextField(verbose_name="User Agent")
    session_key = models.CharField(max_length=40, verbose_name="Session Key")
    is_successful = models.BooleanField(default=True, verbose_name="Đăng nhập thành công")
    failure_reason = models.CharField(max_length=200, blank=True, verbose_name="Lý do thất bại")
    
    class Meta:
        verbose_name = "Lịch sử đăng nhập"
        verbose_name_plural = "Lịch sử đăng nhập"
        ordering = ['-login_time']
        
    def __str__(self):
        status = "Thành công" if self.is_successful else f"Thất bại ({self.failure_reason})"
        return f"{self.user.get_full_name()} - {self.login_time.strftime('%d/%m/%Y %H:%M')} - {status}"
        
    @property
    def session_duration(self):
        """Thời gian phiên làm việc"""
        if self.logout_time:
            return self.logout_time - self.login_time
        return None

class SecurityEvent(models.Model):
    """Sự kiện bảo mật"""
    EVENT_TYPE_CHOICES = [
        ('suspicious_login', 'Đăng nhập đáng ngờ'),
        ('multiple_failed_login', 'Đăng nhập sai nhiều lần'),
        ('permission_denied', 'Truy cập bị từ chối'),
        ('data_breach_attempt', 'Cố gắng vi phạm dữ liệu'),
        ('sql_injection', 'SQL Injection'),
        ('xss_attempt', 'XSS Attack'),
        ('brute_force', 'Brute Force Attack'),
        ('unusual_activity', 'Hoạt động bất thường'),
        ('other', 'Khác'),
    ]
    
    RISK_LEVEL_CHOICES = [
        ('low', 'Thấp'),
        ('medium', 'Trung bình'),
        ('high', 'Cao'),
        ('critical', 'Nghiêm trọng'),
    ]
    
    STATUS_CHOICES = [
        ('detected', 'Phát hiện'),
        ('investigating', 'Đang điều tra'),
        ('resolved', 'Đã giải quyết'),
        ('false_positive', 'Báo động giả'),
    ]
    
    event_type = models.CharField(max_length=30, choices=EVENT_TYPE_CHOICES, verbose_name="Loại sự kiện")
    risk_level = models.CharField(max_length=20, choices=RISK_LEVEL_CHOICES, verbose_name="Mức độ rủi ro")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='detected', verbose_name="Trạng thái")
    
    # Thông tin sự kiện
    title = models.CharField(max_length=200, verbose_name="Tiêu đề")
    description = models.TextField(verbose_name="Mô tả")
    source_ip = models.GenericIPAddressField(verbose_name="IP nguồn")
    target_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='security_events', verbose_name="Người dùng liên quan")
    
    # Dữ liệu kỹ thuật
    request_data = models.JSONField(default=dict, blank=True, verbose_name="Dữ liệu request")
    user_agent = models.TextField(blank=True, verbose_name="User Agent")
    referer = models.URLField(blank=True, verbose_name="Referer")
    
    # Xử lý
    investigated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='investigated_events', verbose_name="Người điều tra")
    resolution_notes = models.TextField(blank=True, verbose_name="Ghi chú giải quyết")
    
    # Thời gian
    detected_at = models.DateTimeField(auto_now_add=True, verbose_name="Thời gian phát hiện")
    resolved_at = models.DateTimeField(null=True, blank=True, verbose_name="Thời gian giải quyết")
    
    class Meta:
        verbose_name = "Sự kiện bảo mật"
        verbose_name_plural = "Sự kiện bảo mật"
        ordering = ['-detected_at']
        
    def __str__(self):
        return f"{self.title} ({self.get_risk_level_display()}) - {self.detected_at.strftime('%d/%m/%Y %H:%M')}"

class DataExportLog(models.Model):
    """Nhật ký xuất dữ liệu"""
    EXPORT_TYPE_CHOICES = [
        ('excel', 'Excel'),
        ('pdf', 'PDF'),
        ('csv', 'CSV'),
        ('json', 'JSON'),
        ('xml', 'XML'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Người xuất")
    export_type = models.CharField(max_length=20, choices=EXPORT_TYPE_CHOICES, verbose_name="Loại file")
    table_name = models.CharField(max_length=100, verbose_name="Bảng dữ liệu")
    record_count = models.PositiveIntegerField(verbose_name="Số bản ghi")
    file_size = models.PositiveIntegerField(verbose_name="Kích thước file (bytes)")
    filters_applied = models.JSONField(default=dict, blank=True, verbose_name="Bộ lọc áp dụng")
    download_count = models.PositiveIntegerField(default=0, verbose_name="Số lần tải")
    file_path = models.CharField(max_length=500, blank=True, verbose_name="Đường dẫn file")
    ip_address = models.GenericIPAddressField(verbose_name="Địa chỉ IP")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Thời gian tạo")
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name="Thời gian hết hạn")
    
    class Meta:
        verbose_name = "Nhật ký xuất dữ liệu"
        verbose_name_plural = "Nhật ký xuất dữ liệu"
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.user.get_full_name()} xuất {self.table_name} ({self.export_type}) - {self.created_at.strftime('%d/%m/%Y %H:%M')}"
