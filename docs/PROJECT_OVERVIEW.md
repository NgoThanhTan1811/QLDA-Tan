# HỆ THỐNG QUẢN LÝ TRÁI CÂY - TỔNG QUAN DỰ ÁN

## 1. THÔNG TIN CHUNG
- **Tên dự án**: Hệ thống quản lý trái cây (Fruit Management System)
- **Ngôn ngữ**: Python Django
- **Database**: MySQL
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Mục đích**: Kết nối nông dân cung cấp trái cây với khách hàng mua sản phẩm

## 2. CẤU TRÚC DỰ ÁN

### 2.1 Apps chính:
- **farmers**: Quản lý nông dân và sản phẩm của họ
- **customers**: Quản lý khách hàng và người mua
- **products**: Quản lý sản phẩm tổng quát
- **orders**: Quản lý đơn hàng và theo dõi
- **inventory**: Quản lý kho hàng
- **payments**: Quản lý thanh toán
- **accounts**: Quản lý tài khoản người dùng
- **dashboard**: Trang tổng quan
- **management**: Quản lý hệ thống
- **activity_logs**: Nhật ký hoạt động
- **utils**: Tiện ích và API
- **import_export**: Xuất nhập dữ liệu

### 2.2 Apps đã loại bỏ:
- ~~**companies**~~: Đã thay thế bằng farmers và customers
- ~~**news**~~: Đã loại bỏ để tập trung vào core business

## 3. CHỨC NĂNG CHI TIẾT

### 3.1 FARMERS (Nông dân - Nhà cung cấp)

#### Models:
- **Farmer**: Thông tin nông dân
  - Mã nông dân (tự động sinh)
  - Thông tin cơ bản (tên, loại hình, liên hệ)
  - Địa chỉ và vùng canh tác
  - Thông tin canh tác (diện tích, kinh nghiệm, cây trồng chính)
  - Chứng nhận (hữu cơ, VietGAP, GlobalGAP, HACCP, ISO)
  - Đánh giá và xếp hạng
  - Trạng thái (đã xác minh, hoạt động, nổi bật)

- **FarmingArea**: Khu vực canh tác
  - Tên khu vực, diện tích
  - Loại đất, nguồn nước
  - Tọa độ GPS
  - Mô tả chi tiết

- **CropProduct**: Sản phẩm nông nghiệp
  - Thông tin sản phẩm (tên, giống/loại)
  - Thời gian canh tác (gieo trồng, thu hoạch)
  - Sản lượng và chất lượng
  - Giá cả và số lượng đặt hàng tối thiểu
  - Chứng nhận sản phẩm
  - Phương pháp canh tác, thu hoạch, bảo quản

- **FarmerDocument**: Tài liệu của nông dân
  - CMND/CCCD, giấy phép kinh doanh
  - Giấy chứng nhận quyền sử dụng đất
  - Các chứng nhận chất lượng

#### Chức năng:
- Đăng ký và quản lý thông tin nông dân
- Quản lý khu vực canh tác
- Đăng bán sản phẩm với thông tin chi tiết
- Theo dõi đơn hàng và thanh toán
- Quản lý tài liệu và chứng nhận

### 3.2 CUSTOMERS (Khách hàng - Người mua)

#### Models:
- **Customer**: Thông tin khách hàng
  - Mã khách hàng (tự động sinh)
  - Liên kết với User account (nếu có)
  - Thông tin cơ bản (tên, loại khách hàng, liên hệ)
  - Địa chỉ giao hàng
  - Thông tin doanh nghiệp (nếu có)
  - Cấp thành viên (đồng, bạc, vàng, bạch kim, kim cương)
  - Sở thích mua sắm
  - Thống kê mua sắm

- **CustomerAddress**: Địa chỉ giao hàng
  - Nhà riêng, văn phòng, kho hàng
  - Thông tin người nhận
  - Địa chỉ mặc định

- **CustomerReview**: Đánh giá của khách hàng
  - Đánh giá nông dân và sản phẩm
  - Chất lượng sản phẩm, thời gian giao hàng, dịch vụ
  - Đánh giá đã xác thực

- **CustomerWishlist**: Danh sách yêu thích
  - Theo dõi nông dân và sản phẩm ưa thích

- **CustomerDocument**: Tài liệu khách hàng
  - CMND/CCCD, giấy phép kinh doanh
  - Hợp đồng và tài liệu liên quan

#### Chức năng:
- Đăng ký và quản lý tài khoản
- Tìm kiếm và lọc sản phẩm
- Đặt hàng và theo dõi đơn hàng
- Đánh giá nông dân và sản phẩm
- Quản lý danh sách yêu thích
- Quản lý địa chỉ giao hàng

### 3.3 ORDERS (Đơn hàng - Theo dõi nâng cao)

#### Models cập nhật:
- **Order**: Đơn hàng
  - Liên kết với Farmer (đơn mua) hoặc Customer (đơn bán)
  - Loại đơn hàng: mua từ nông dân, bán cho khách hàng, xuất khẩu, nội bộ
  - Trạng thái chi tiết: nháp → xác nhận → xử lý → chuẩn bị → đóng gói → giao vận → vận chuyển → giao hàng → hoàn thành
  - Độ ưu tiên (thấp, trung bình, cao, khẩn cấp)
  - Thông tin theo dõi (số vận đơn, trọng lượng)

- **OrderTracking**: Theo dõi chi tiết đơn hàng
  - Thay đổi trạng thái
  - Cập nhật vị trí (GPS)
  - Ghi chú và báo cáo vấn đề
  - Tải tài liệu
  - Nhận thanh toán

- **OrderStatusHistory**: Lịch sử thay đổi trạng thái
- **OrderDocument**: Tài liệu đơn hàng

#### Tính năng theo dõi cho Admin:
- Dashboard theo dõi tất cả đơn hàng
- Lọc theo trạng thái, độ ưu tiên, ngày
- Cập nhật trạng thái hàng loạt
- Xuất báo cáo đơn hàng
- Thông báo tự động cho khách hàng

### 3.4 PRODUCTS (Sản phẩm tổng quát)
- Catalog sản phẩm hệ thống
- Danh mục và phân loại
- Thông tin dinh dưỡng
- Hình ảnh sản phẩm

### 3.5 INVENTORY (Kho hàng)
- Quản lý tồn kho
- Nhập xuất kho
- Kiểm kê định kỳ
- Cảnh báo hết hàng

### 3.6 PAYMENTS (Thanh toán)
- Quản lý hóa đơn
- Theo dõi thanh toán
- Báo cáo tài chính
- Tích hợp cổng thanh toán

### 3.7 DASHBOARD (Trang tổng quan)
- Thống kê tổng quan
- Biểu đồ doanh thu
- Top nông dân/khách hàng
- Đơn hàng cần xử lý
- Cảnh báo hệ thống

### 3.8 MANAGEMENT (Quản lý hệ thống)
- Quản lý người dùng
- Phân quyền
- Cấu hình hệ thống
- Backup dữ liệu

## 4. WORKFLOW CHÍNH

### 4.1 Quy trình nông dân:
1. Đăng ký tài khoản nông dân
2. Xác minh thông tin và tài liệu
3. Thêm khu vực canh tác
4. Đăng bán sản phẩm
5. Nhận đơn hàng từ khách hàng
6. Chuẩn bị và giao hàng
7. Nhận thanh toán

### 4.2 Quy trình khách hàng:
1. Đăng ký tài khoản
2. Tìm kiếm sản phẩm
3. Xem thông tin nông dân và đánh giá
4. Đặt hàng
5. Theo dõi đơn hàng
6. Nhận hàng và thanh toán
7. Đánh giá nông dân/sản phẩm

### 4.3 Quy trình admin theo dõi đơn hàng:
1. Monitor tất cả đơn hàng real-time
2. Cập nhật trạng thái đơn hàng
3. Xử lý vấn đề và khiếu nại
4. Thông báo cho khách hàng
5. Tạo báo cáo và thống kê

## 5. TÍNH NĂNG ĐẶC BIỆT

### 5.1 Theo dõi chất lượng:
- Truy xuất nguồn gốc sản phẩm
- Lịch sử canh tác và thu hoạch
- Chứng nhận chất lượng
- Đánh giá từ khách hàng

### 5.2 Hệ thống đánh giá:
- Đánh giá đa chiều (sản phẩm, giao hàng, dịch vụ)
- Xếp hạng nông dân
- Cấp thành viên khách hàng
- Điểm thưởng và ưu đãi

### 5.3 Báo cáo và thống kê:
- Dashboard thời gian thực
- Báo cáo doanh thu theo thời gian
- Phân tích xu hướng mua sắm
- Hiệu suất nông dân
- Chất lượng dịch vụ

## 6. CÔNG NGHỆ SỬ DỤNG

### Backend:
- Django 4.2+
- MySQL Database
- Django REST Framework (API)
- Django Admin (quản trị)

### Frontend:
- HTML5, CSS3, JavaScript
- Bootstrap 4/5
- jQuery
- Chart.js (biểu đồ)

### Tích hợp:
- Email notification
- SMS gateway
- Payment gateway
- GPS tracking
- File upload/download

## 7. TRIỂN KHAI

### Development:
- Local development server
- SQLite/MySQL database
- Debug mode enabled

### Production:
- Web server (Nginx/Apache)
- Database server (MySQL/PostgreSQL)
- Media file storage
- SSL certificate
- Backup system

## 8. BẢO MẬT

- User authentication
- Role-based permissions
- Data encryption
- Input validation
- CSRF protection
- SQL injection prevention

---

**Ghi chú**: Dự án tập trung vào việc kết nối trực tiếp giữa nông dân (nguồn cung) và khách hàng (nguồn cầu), đảm bảo chất lượng sản phẩm và trải nghiệm người dùng tốt nhất.
