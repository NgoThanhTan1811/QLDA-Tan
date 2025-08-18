# 🍎 Hệ thống Quản lý Xuất nhập khẩu Trái cây - PROJECT OVERVIEW

## 📊 Tổng quan dự án

**Fruit Export Management System** là hệ thống quản lý toàn diện cho hoạt động xuất nhập khẩu nông sản, được thiết kế theo mô hình marketplace kết nối trang trại với khách hàng.

## 🏗️ Kiến trúc hệ thống

### 🌱 **Farmers (Trang trại - Nguồn cung)**
- Quản lý thông tin nông dân và trang trại
- Theo dõi diện tích canh tác và sản phẩm
- Chứng nhận nông nghiệp (organic, VietGAP, GlobalGAP)
- Đánh giá và xếp hạng chất lượng

### 👥 **Customers (Khách hàng - Nguồn cầu)**
- Quản lý khách hàng cá nhân và doanh nghiệp
- Hệ thống thành viên từ bronze đến diamond
- Địa chỉ giao hàng và lịch sử mua hàng
- Đánh giá sản phẩm và wishlist

### 🍎 **Products (Sản phẩm)**
- Catalog sản phẩm nông nghiệp
- Phân loại theo danh mục và xuất xứ
- Thông tin dinh dưỡng và chứng nhận
- Giá cả và tồn kho

### 📦 **Orders (Đơn hàng)**
- Quản lý đơn hàng từ farmers đến customers
- Theo dõi trạng thái real-time với GPS
- Lịch sử thay đổi và ưu tiên
- Tích hợp thanh toán

### 🏪 **Inventory (Kho hàng)**
- Quản lý tồn kho đa kho
- Theo dõi nhập/xuất hàng
- Cảnh báo hết hàng
- Báo cáo biến động

### 💳 **Payments (Thanh toán)**
- Quản lý thanh toán và hóa đơn
- Nhiều phương thức thanh toán
- Theo dõi công nợ
- Báo cáo tài chính

### 👨‍💼 **Management (Quản lý)**
- Dashboard tổng quan cho admin
- Quản lý nhân viên và phân quyền
- Thống kê và báo cáo
- Import/Export dữ liệu

### 📊 **Dashboard (Bảng điều khiển)**
- Thống kê tổng quan hệ thống
- Charts và biểu đồ
- Key Performance Indicators
- Quick actions

### 👤 **Accounts (Tài khoản)**
- Quản lý user và authentication
- Profile và settings
- Role-based access control
- Activity tracking

## 🎯 **Tính năng nổi bật**

### 📱 **Real-time Order Tracking**
- GPS tracking cho giao hàng
- Cập nhật trạng thái tự động
- Notifications real-time
- History tracking

### 🌾 **Agricultural Focus**
- Quản lý vùng canh tác
- Theo dõi mùa vụ
- Chứng nhận nông nghiệp
- Truy xuất nguồn gốc

### 🎖️ **Customer Loyalty**
- Hệ thống membership tiers
- Reward points
- Special pricing
- VIP services

### 📈 **Analytics & Reporting**
- Sales analytics
- Inventory reports
- Customer insights
- Market trends

## 🛠️ **Công nghệ sử dụng**

### Backend
- **Framework**: Django 4.2+
- **Database**: MySQL 8.0
- **API**: Django REST Framework
- **Authentication**: Django Auth + JWT

### Frontend
- **Template Engine**: Django Templates
- **CSS Framework**: Bootstrap 5
- **JavaScript**: jQuery + Vanilla JS
- **Charts**: Chart.js
- **Icons**: Font Awesome

### Infrastructure
- **Web Server**: Nginx (production)
- **WSGI**: Gunicorn (production)
- **Static Files**: Django Collectstatic
- **Media Files**: Local storage / Cloud storage

## 📁 **Cấu trúc thư mục**

```
QLDA/
├── manage.py
├── requirements.txt
├── README.md
├── fruit_manage/          # Django project settings
├── accounts/              # User management
├── farmers/               # Farmer/farm management  
├── customers/             # Customer management
├── products/              # Product catalog
├── orders/                # Order processing
├── payments/              # Payment processing
├── inventory/             # Inventory management
├── dashboard/             # Analytics dashboard
├── management/            # Admin management
├── activity_logs/         # System logging
├── import_export/         # Data import/export
├── utils/                 # Utilities and APIs
├── static/                # Static files (CSS, JS, images)
├── templates/             # HTML templates
└── docs/                  # Documentation
```

## 🔐 **Bảo mật**

- User authentication & authorization
- Role-based access control (RBAC)
- Input validation và sanitization
- CSRF protection
- SQL injection prevention
- Secure password hashing

## 📊 **Database Schema**

### Core Entities
- **Farmers**: Thông tin trang trại và nông dân
- **Customers**: Thông tin khách hàng và doanh nghiệp
- **Products**: Catalog sản phẩm nông nghiệp
- **Orders**: Đơn hàng và order details
- **Payments**: Thanh toán và hóa đơn
- **Inventory**: Tồn kho và biến động

### Relationships
- Farmers → Products (1-nhiều)
- Customers → Orders (1-nhiều) 
- Orders → OrderDetails (1-nhiều)
- Orders → Payments (1-1)
- Products → Inventory (1-nhiều)

## 🚀 **Deployment**

### Development
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Production
- Nginx + Gunicorn
- MySQL database
- SSL/TLS certificates
- Static files serving
- Media files handling

## 📈 **Performance**

- Database indexing
- Query optimization
- Caching strategies
- Pagination
- Lazy loading
- Image optimization

## 🔄 **API Integration**

- RESTful APIs cho mobile apps
- Third-party payment gateways
- SMS/Email notifications
- Export/Import tools
- External logistics APIs

## 📚 **Documentation**

- [Database Schema](docs/DATABASE_SCHEMA.md)
- [User Guide](docs/USER_GUIDE.md) 
- [API Documentation](docs/API_DOCS.md)
- [Deployment Guide](docs/DEPLOYMENT.md)

## 👥 **Team & Contact**

- **Project Manager**: [Tên PM]
- **Lead Developer**: [Tên Lead Dev]
- **Frontend Developer**: [Tên FE Dev]
- **Database Admin**: [Tên DBA]

---

*Cập nhật lần cuối: August 18, 2025*
*Version: 2.0.0 (Migrated from Companies to Farmers/Customers)*
