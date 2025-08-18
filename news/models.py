from django.db import models
from accounts.models import User

class NewsCategory(models.Model):
    """Danh mục tin tức"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Tên danh mục")
    description = models.TextField(blank=True, verbose_name="Mô tả")
    color = models.CharField(max_length=7, default='#007bff', verbose_name="Màu sắc")
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    
    class Meta:
        verbose_name = "Danh mục tin tức"
        verbose_name_plural = "Danh mục tin tức"
        ordering = ['name']
        
    def __str__(self):
        return self.name

class News(models.Model):
    """Tin tức"""
    NEWS_TYPE_CHOICES = [
        ('internal', 'Tin nội bộ'),
        ('industry', 'Tin ngành'),
        ('system', 'Thông báo hệ thống'),
        ('regulation', 'Quy định mới'),
        ('market', 'Thị trường'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Nháp'),
        ('published', 'Đã xuất bản'),
        ('archived', 'Lưu trữ'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Thấp'),
        ('normal', 'Bình thường'),
        ('high', 'Cao'),
        ('urgent', 'Khẩn cấp'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Tiêu đề")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Slug")
    summary = models.TextField(max_length=500, verbose_name="Tóm tắt")
    content = models.TextField(verbose_name="Nội dung")
    
    # Phân loại
    category = models.ForeignKey(NewsCategory, on_delete=models.CASCADE, related_name='news', verbose_name="Danh mục")
    news_type = models.CharField(max_length=20, choices=NEWS_TYPE_CHOICES, verbose_name="Loại tin")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal', verbose_name="Độ ưu tiên")
    
    # Trạng thái
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="Trạng thái")
    is_featured = models.BooleanField(default=False, verbose_name="Tin nổi bật")
    is_pinned = models.BooleanField(default=False, verbose_name="Ghim tin")
    
    # Hình ảnh
    featured_image = models.ImageField(upload_to='news/', blank=True, null=True, verbose_name="Hình ảnh đại diện")
    
    # Ngày tháng
    publish_date = models.DateTimeField(blank=True, null=True, verbose_name="Ngày xuất bản")
    expire_date = models.DateTimeField(blank=True, null=True, verbose_name="Ngày hết hạn")
    
    # Thống kê
    view_count = models.PositiveIntegerField(default=0, verbose_name="Lượt xem")
    
    # Thông tin người tạo
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_news', verbose_name="Tác giả")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    
    class Meta:
        verbose_name = "Tin tức"
        verbose_name_plural = "Tin tức"
        ordering = ['-is_pinned', '-publish_date', '-created_at']
        
    def __str__(self):
        return self.title
        
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            import uuid
            self.slug = slugify(self.title) + '-' + str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)

class NewsComment(models.Model):
    """Bình luận tin tức"""
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments', verbose_name="Tin tức")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Người bình luận")
    content = models.TextField(verbose_name="Nội dung")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies', verbose_name="Bình luận gốc")
    is_active = models.BooleanField(default=True, verbose_name="Đang hiển thị")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    
    class Meta:
        verbose_name = "Bình luận"
        verbose_name_plural = "Bình luận"
        ordering = ['created_at']
        
    def __str__(self):
        return f"{self.author.get_full_name()} - {self.news.title}"

class NewsView(models.Model):
    """Lịch sử xem tin tức"""
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Người xem")
    ip_address = models.GenericIPAddressField(verbose_name="Địa chỉ IP")
    user_agent = models.TextField(verbose_name="User Agent")
    viewed_at = models.DateTimeField(auto_now_add=True, verbose_name="Thời gian xem")
    
    class Meta:
        verbose_name = "Lượt xem tin tức"
        verbose_name_plural = "Lượt xem tin tức"
        unique_together = ['news', 'user', 'ip_address']
        
    def __str__(self):
        return f"{self.user.get_full_name()} xem {self.news.title}"

class SystemNotification(models.Model):
    """Thông báo hệ thống"""
    NOTIFICATION_TYPE_CHOICES = [
        ('info', 'Thông tin'),
        ('warning', 'Cảnh báo'),
        ('error', 'Lỗi'),
        ('success', 'Thành công'),
        ('maintenance', 'Bảo trì'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Tiêu đề")
    message = models.TextField(verbose_name="Nội dung")
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES, verbose_name="Loại thông báo")
    
    # Đối tượng nhận
    target_users = models.ManyToManyField(User, blank=True, verbose_name="Người nhận cụ thể")
    target_roles = models.CharField(max_length=200, blank=True, help_text="Các role cách nhau bằng dấu phẩy", verbose_name="Vai trò nhận")
    is_global = models.BooleanField(default=False, verbose_name="Thông báo toàn hệ thống")
    
    # Trạng thái
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")
    start_date = models.DateTimeField(verbose_name="Thời gian bắt đầu")
    end_date = models.DateTimeField(blank=True, null=True, verbose_name="Thời gian kết thúc")
    
    # Thông tin tạo
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_notifications', verbose_name="Người tạo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    
    class Meta:
        verbose_name = "Thông báo hệ thống"
        verbose_name_plural = "Thông báo hệ thống"
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title

class NotificationRead(models.Model):
    """Trạng thái đọc thông báo"""
    notification = models.ForeignKey(SystemNotification, on_delete=models.CASCADE, related_name='read_status')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Người đọc")
    read_at = models.DateTimeField(auto_now_add=True, verbose_name="Thời gian đọc")
    
    class Meta:
        verbose_name = "Trạng thái đọc thông báo"
        verbose_name_plural = "Trạng thái đọc thông báo"
        unique_together = ['notification', 'user']
        
    def __str__(self):
        return f"{self.user.get_full_name()} đã đọc {self.notification.title}"
