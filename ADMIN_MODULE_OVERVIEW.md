# Tổng hợp chức năng và bảng database chính của các module admin

## 1. Chức năng đã làm được

### Quản lý tài khoản (accounts)
- Quản lý User, UserProfile
- Tùy chỉnh giao diện admin cho User, UserProfile

### Quản lý công ty (companies)
- Quản lý Company, CompanyDocument
- Inline quản lý tài liệu công ty

### Quản lý khách hàng (customers)
- Quản lý Customer, CustomerAddress, CustomerReview, CustomerWishlist, CustomerDocument
- Inline quản lý địa chỉ, tài liệu, đánh giá, wishlist

### Quản lý nông dân (farmers)
- Quản lý Farmer, FarmingArea, CropProduct, FarmerDocument
- Inline quản lý vùng trồng, sản phẩm, tài liệu

### Quản lý sản phẩm (products)
- Quản lý Category, Unit, Product, ProductImage, ProductSpecification
- Inline quản lý hình ảnh, thông số sản phẩm

### Quản lý đơn hàng (orders)
- Quản lý Order, OrderDetail, OrderStatusHistory, OrderTracking, OrderDocument

### Quản lý thanh toán (payments)
- Quản lý Payment, PaymentDocument, PaymentSchedule, ExchangeRate

### Quản lý kho (inventory)
- Quản lý Warehouse, InventoryStock, StockMovement, StockTaking, StockTakingDetail

### Quản lý nhân sự (management)
- Quản lý Employee, Customer

### Quản lý nhật ký hoạt động (activity_logs)
- Quản lý ActivityLog, LoginHistory, SecurityEvent, DataExportLog

### Quản lý xuất nhập khẩu (import_export)
- Quản lý ImportExportDocument, CustomsDeclaration, ShippingDocument

### Quản lý tin tức (news)
- Quản lý NewsCategory, News, NewsComment, NewsView, SystemNotification, NotificationRead

## 2. Các bảng database chính

- accounts: User, UserProfile
- companies: Company, CompanyDocument, UpdateCompany
- customers: Customer, CustomerAddress, CustomerReview, CustomerWishlist, CustomerDocument
- farmers: Farmer, FarmingArea, CropProduct, FarmerDocument
- products: Category, Unit, Product, ProductImage, ProductSpecification
- orders: Order, OrderDetail, OrderStatusHistory, OrderTracking, OrderDocument
- payments: Payment, PaymentDocument, PaymentSchedule, ExchangeRate
- inventory: Warehouse, InventoryStock, StockMovement, StockTaking, StockTakingDetail
- management: Employee, Customer
- activity_logs: ActivityLog, LoginHistory, SecurityEvent, DataExportLog
- import_export: ImportExportDocument, CustomsDeclaration, ShippingDocument
- news: NewsCategory, News, NewsComment, NewsView, SystemNotification, NotificationRead

---
*File tổng hợp này liệt kê các chức năng đã làm được và các bảng dữ liệu chính của từng module admin trong hệ thống QLDA-Tan.*
