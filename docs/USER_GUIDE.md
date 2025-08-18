# Hướng Dẫn Sử Dụng Hệ Thống Quản Lý Xuất Nhập Khẩu Trái Cây

## 📋 Mục lục
1. [Tổng quan hệ thống](#tổng-quan-hệ-thống)
2. [Đăng nhập và bảo mật](#đăng-nhập-và-bảo-mật)
3. [Quản lý sản phẩm](#quản-lý-sản-phẩm)
4. [Quản lý đơn hàng](#quản-lý-đơn-hàng)
5. [Quản lý kho hàng](#quản-lý-kho-hàng)
6. [Quản lý đối tác](#quản-lý-đối-tác)
7. [Thanh toán](#thanh-toán)
8. [Báo cáo và thống kê](#báo-cáo-và-thống-kê)

---

## 🎯 Tổng quan hệ thống

### Mục đích
Hệ thống được thiết kế để quản lý toàn bộ quy trình xuất nhập khẩu trái cây từ A đến Z, bao gồm:
- Quản lý sản phẩm và danh mục
- Theo dõi tồn kho và kho bãi
- Xử lý đơn hàng xuất/nhập khẩu
- Quản lý đối tác (khách hàng, nhà cung cấp)
- Xử lý thanh toán và tài chính
- Báo cáo và phân tích dữ liệu

### Phân quyền người dùng
- **Admin**: Toàn quyền quản lý hệ thống
- **Manager**: Quản lý đơn hàng, sản phẩm, đối tác
- **Staff**: Nhập liệu, cập nhật đơn hàng
- **Accountant**: Quản lý thanh toán, báo cáo tài chính

---

## 🔐 Đăng nhập và bảo mật

### Tài khoản mặc định
- **Username**: `admin`
- **Password**: `admin123`
- **Vai trò**: Administrator

### Đăng nhập
1. Truy cập: `http://127.0.0.1:8000`
2. Nhập username và password
3. Hệ thống sẽ chuyển hướng đến Dashboard

### Thay đổi mật khẩu
1. Click vào tên người dùng ở góc phải
2. Chọn "Hồ sơ cá nhân"
3. Click "Đổi mật khẩu"
4. Nhập mật khẩu cũ và mật khẩu mới

---

## 🍎 Quản lý sản phẩm

### Xem danh sách sản phẩm
1. Vào menu "Sản phẩm" → "Danh sách sản phẩm"
2. Hiển thị: Mã SP, tên, danh mục, xuất xứ, giá bán, trạng thái

### Thêm sản phẩm mới
1. Click "Thêm sản phẩm" 
2. Điền thông tin:
   - **Mã sản phẩm**: Tự động tạo (SP-XXXX)
   - **Tên sản phẩm**: VD: "Thanh long ruột đỏ"
   - **Danh mục**: Trái cây nhiệt đới, có múi...
   - **Xuất xứ**: Tỉnh/thành sản xuất
   - **Chất lượng**: A, B, C
   - **Giá cost**: Giá nhập (VNĐ)
   - **Giá bán**: Giá bán nội địa (VNĐ)
   - **Giá xuất khẩu**: Giá xuất khẩu (USD)
   - **Thông số kỹ thuật**: Nhiệt độ bảo quản, độ ẩm...

### Quản lý danh mục
1. Vào "Sản phẩm" → "Danh mục"
2. Tạo danh mục: Trái cây nhiệt đới, Trái cây có múi, Trái cây khô...

---

## 🛒 Quản lý đơn hàng

### Tạo đơn hàng xuất khẩu
1. Vào "Đơn hàng" → "Tạo đơn hàng"
2. Chọn loại: **Xuất khẩu**
3. Thông tin cơ bản:
   - **Khách hàng**: Chọn từ danh sách đối tác
   - **Ngày giao hàng**: Dự kiến
   - **Địa chỉ giao hàng**: Cảng, địa chỉ nhận
4. Thêm sản phẩm:
   - Chọn sản phẩm
   - Số lượng (kg/tấn)
   - Giá đơn vị (USD)
5. Thông tin vận chuyển:
   - Phương thức: Đường hàng không, đường biển
   - Điều kiện: FOB, CIF, EXW...

### Tạo đơn hàng nhập khẩu
1. Chọn loại: **Nhập khẩu**
2. **Nhà cung cấp**: Chọn supplier
3. Quy trình tương tự xuất khẩu

### Theo dõi trạng thái đơn hàng
- **Chờ xác nhận**: Mới tạo, đang đợi duyệt
- **Đã xác nhận**: Đã duyệt, chuẩn bị hàng
- **Đang xử lý**: Đang chuẩn bị, đóng gói
- **Đã giao**: Đã xuất kho, giao vận chuyển
- **Hoàn thành**: Đã giao thành công
- **Đã hủy**: Đơn hàng bị hủy

---

## 📦 Quản lý kho hàng

### Xem tồn kho
1. Vào "Kho hàng" → "Tồn kho"
2. Hiển thị:
   - Sản phẩm và số lượng hiện tại
   - Tồn kho tối thiểu/tối đa
   - Cảnh báo sắp hết hàng
   - Giá trị tồn kho

### Nhập kho
1. Click "Nhập kho" ở trang tồn kho
2. Chọn:
   - **Kho nhận**: Kho Trung tâm, Kho Cần Thơ...
   - **Sản phẩm**: Từ dropdown
   - **Số lượng nhập**
   - **Giá nhập** (nếu có)
   - **Ghi chú**: Lý do nhập, nguồn hàng

### Xuất kho  
1. Click "Xuất kho"
2. Thông tin tương tự nhập kho
3. **Lý do xuất**: Bán hàng, hỏng hóc, chuyển kho...

### Quản lý kho bãi
1. Vào "Kho hàng" → "Quản lý kho"
2. Thêm kho mới:
   - **Tên kho**: VD: "Kho Đà Nẵng"
   - **Mã kho**: KHO-DN
   - **Địa chỉ**: Địa chỉ chi tiết
   - **Người quản lý**: Chọn từ danh sách nhân viên
   - **Sức chứa**: Tấn

---

## 🏢 Quản lý đối tác

### Thêm khách hàng
1. Vào "Đối tác" → "Thêm đối tác"
2. Chọn loại: **Khách hàng**
3. Thông tin:
   - **Tên công ty**: VD: "Fresh Fruit USA Inc."
   - **Mã số thuế**: Tax code của công ty
   - **Địa chỉ**: Địa chỉ trụ sở
   - **Email/Phone**: Liên lạc chính
   - **Người liên hệ**: Tên, phone, email
   - **Giấy phép**: Export/Import license (nếu có)

### Thêm nhà cung cấp
1. Chọn loại: **Nhà cung cấp**
2. Thông tin tương tự khách hàng
3. Thêm:
   - **Sản phẩm cung cấp**: Loại trái cây
   - **Vùng cung cấp**: Tỉnh/thành
   - **Chứng chỉ chất lượng**: VietGAP, GlobalGAP...

### Quản lý tài liệu
1. Vào chi tiết đối tác
2. Tab "Tài liệu"
3. Upload:
   - Giấy phép kinh doanh
   - Chứng chỉ xuất nhập khẩu
   - Hợp đồng hợp tác
   - Giấy chứng nhận chất lượng

---

## 💰 Thanh toán

### Tạo phiếu thanh toán
1. Vào "Thanh toán" → "Danh sách thanh toán"
2. Click "Tạo thanh toán"
3. Chọn:
   - **Đơn hàng**: Từ danh sách đơn đã xác nhận
   - **Loại thanh toán**: Tiền cọc, thanh toán cuối...
   - **Số tiền**: USD hoặc VNĐ
   - **Phương thức**: Chuyển khoản, L/C, Cash...
   - **Ngân hàng**: Thông tin tài khoản

### Theo dõi tỷ giá
1. Vào "Thanh toán" → "Tỷ giá"
2. Cập nhật tỷ giá USD/VNĐ hằng ngày
3. Hệ thống tự động tính toán giá trị VNĐ

### Trạng thái thanh toán
- **Chờ thanh toán**: Chưa nhận được tiền
- **Thanh toán 1 phần**: Đã nhận 1 phần
- **Đã thanh toán**: Nhận đủ tiền
- **Đã hoàn tiền**: Hoàn lại khách hàng

---

## 📊 Báo cáo và thống kê

### Dashboard tổng quan
- **Tổng đơn hàng**: Số lượng và giá trị
- **Doanh thu**: Theo tháng, quý
- **Tồn kho**: Tình trạng hiện tại
- **Cảnh báo**: Sắp hết hàng, đơn quá hạn

### Báo cáo doanh thu
1. Vào "Báo cáo" → "Doanh thu"
2. Chọn:
   - **Thời gian**: Tháng, quý, năm
   - **Loại**: Xuất khẩu, nhập khẩu
   - **Sản phẩm**: Tất cả hoặc cụ thể
   - **Thị trường**: Theo quốc gia

### Báo cáo tồn kho
1. Vào "Báo cáo" → "Tồn kho"
2. Xuất Excel báo cáo:
   - Tồn kho theo sản phẩm
   - Biến động nhập/xuất
   - Giá trị tồn kho

### Báo cáo khách hàng
1. Danh sách khách hàng VIP
2. Doanh số theo khách hàng
3. Công nợ phải thu

---

## 🚀 Quy trình nghiệp vụ chuẩn

### Quy trình xuất khẩu hoàn chỉnh
1. **Nhận đơn hàng**:
   - Khách hàng gửi yêu cầu báo giá
   - Tạo báo giá trong hệ thống
   - Khách hàng xác nhận đặt hàng

2. **Tạo đơn hàng**:
   - Tạo đơn xuất khẩu trong hệ thống
   - Xác nhận tồn kho đủ hàng
   - Gửi contract cho khách hàng

3. **Chuẩn bị hàng**:
   - Kiểm tra chất lượng sản phẩm
   - Đóng gói theo yêu cầu
   - Chuẩn bị giấy tờ xuất khẩu

4. **Xuất kho**:
   - Tạo phiếu xuất kho
   - Cập nhật tồn kho
   - Vận chuyển đến cảng

5. **Thanh toán**:
   - Gửi hóa đơn cho khách
   - Theo dõi thanh toán
   - Cập nhật trạng thái

### Quy trình nhập khẩu
1. **Đặt hàng nhà cung cấp**
2. **Theo dõi vận chuyển**
3. **Thủ tục hải quan**
4. **Nhập kho và kiểm tra**
5. **Thanh toán nhà cung cấp**

---

## ⚠️ Lưu ý quan trọng

### Bảo mật dữ liệu
- Thường xuyên backup database
- Không chia sẻ tài khoản admin
- Đăng xuất sau khi sử dụng

### Sao lưu dữ liệu
```bash
# Backup database
python manage.py dumpdata > backup.json

# Restore database  
python manage.py loaddata backup.json
```

### Liên hệ hỗ trợ
- **Email**: support@fruitexport.vn
- **Phone**: 028-1234-5678
- **Thời gian**: 8:00 - 17:30 (T2-T6)

---

## 📝 FAQ - Câu hỏi thường gặp

**Q: Làm sao để thay đổi tỷ giá USD/VNĐ?**
A: Vào "Thanh toán" → "Tỷ giá" → "Cập nhật tỷ giá"

**Q: Tại sao không thể tạo đơn hàng?**
A: Kiểm tra tồn kho, quyền user, và thông tin đối tác đầy đủ

**Q: Làm sao xuất báo cáo Excel?**
A: Mỗi trang danh sách đều có nút "Xuất Excel" ở góc phải

**Q: Quên mật khẩu admin thì làm sao?**
A: Liên hệ IT để reset hoặc dùng lệnh Django trong terminal

---

*Hướng dẫn này được cập nhật thường xuyên. Phiên bản hiện tại: v1.0 - Ngày 08/08/2025*
