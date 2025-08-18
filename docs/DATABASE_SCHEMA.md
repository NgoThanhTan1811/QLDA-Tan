# Database Schema - Hệ thống quản lý xuất nhập khẩu trái cây

## 📋 Tổng quan Database Schema

### Danh sách bảng chính
1. **accounts_customuser** - Quản lý người dùng
2. **companies_company** - Thông tin công ty/đối tác  
3. **products_product** - Sản phẩm trái cây
4. **inventory_inventorystock** - Tồn kho
5. **orders_order** - Đơn hàng xuất/nhập khẩu
6. **payments_payment** - Thanh toán
7. **import_export_customsdeclaration** - Tờ khai hải quan
8. **news_news** - Tin tức

---

## 🗃️ Chi tiết từng bảng

### 1. accounts_customuser (Người dùng)
```sql
CREATE TABLE accounts_customuser (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(150) UNIQUE NOT NULL,
    email VARCHAR(254) UNIQUE NOT NULL,
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    phone VARCHAR(20),
    role VARCHAR(20) DEFAULT 'staff',
    avatar VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    is_staff BOOLEAN DEFAULT FALSE,
    is_superuser BOOLEAN DEFAULT FALSE,
    date_joined DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME,
    password VARCHAR(128) NOT NULL
);
```

**Dữ liệu mẫu:**
```sql
INSERT INTO accounts_customuser VALUES
(1, 'admin', 'admin@company.com', 'Admin', 'System', '0909000000', 'admin', '', 1, 1, 1, NOW(), NOW(), 'pbkdf2_sha256$...'),
(2, 'manager1', 'manager@company.com', 'Nguyễn', 'Quản Lý', '0909123456', 'manager', '', 1, 0, 0, NOW(), NOW(), 'pbkdf2_sha256$...'),
(3, 'staff1', 'staff@company.com', 'Trần', 'Nhân Viên', '0909123457', 'staff', '', 1, 0, 0, NOW(), NOW(), 'pbkdf2_sha256$...');
```

### 2. companies_company (Công ty/Đối tác)
```sql
CREATE TABLE companies_company (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    company_type VARCHAR(20) NOT NULL,
    tax_code VARCHAR(50) UNIQUE,
    address TEXT,
    phone VARCHAR(20),
    email VARCHAR(254),
    website VARCHAR(200),
    contact_person VARCHAR(255),
    contact_phone VARCHAR(20),
    contact_email VARCHAR(254),
    export_license VARCHAR(100),
    import_license VARCHAR(100),
    notes TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

**Dữ liệu mẫu:**
```sql
INSERT INTO companies_company VALUES
(1, 'Công ty TNHH Xuất Nhập Khẩu Trái Cây Việt Nam', 'our_company', '0123456789', '123 Đường ABC, Quận 1, TP.HCM', '028-12345678', 'info@fruitexport.vn', 'www.fruitexport.vn', 'Nguyễn Văn A', '0909123456', 'nguyena@fruitexport.vn', 'XK-001/2023', 'NK-001/2023', '', 1, NOW(), NOW()),
(2, 'Fresh Fruit USA Inc.', 'customer', 'US123456789', '123 Main St, New York, USA', '+1-555-123-4567', 'orders@freshfruit-usa.com', 'www.freshfruit-usa.com', 'John Smith', '+1-555-123-4567', 'john@freshfruit-usa.com', '', '', '', 1, NOW(), NOW()),
(3, 'Hợp tác xã Trái cây Đồng Nai', 'supplier', '9876543210', 'Huyện Long Khánh, Tỉnh Đồng Nai', '0251-123456', 'htx@dongnai-fruit.vn', '', 'Lê Thị B', '0909876543', 'lethib@dongnai-fruit.vn', '', '', '', 1, NOW(), NOW());
```

### 3. products_category (Danh mục sản phẩm)
```sql
CREATE TABLE products_category (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**Dữ liệu mẫu:**
```sql
INSERT INTO products_category VALUES
(1, 'Trái cây nhiệt đới', 'Các loại trái cây nhiệt đới xuất khẩu', 1, NOW()),
(2, 'Trái cây có múi', 'Cam, quýt, bưởi và các loại có múi', 1, NOW());
```

### 4. products_unit (Đơn vị tính)
```sql
CREATE TABLE products_unit (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    symbol VARCHAR(10) NOT NULL
);
```

**Dữ liệu mẫu:**
```sql
INSERT INTO products_unit VALUES
(1, 'Kilogram', 'kg'),
(2, 'Tấn', 'tấn'),
(3, 'Thùng', 'thùng');
```

### 5. products_product (Sản phẩm)
```sql
CREATE TABLE products_product (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    category_id BIGINT,
    unit_id BIGINT,
    description TEXT,
    origin VARCHAR(255),
    quality_grade VARCHAR(10),
    cost_price DECIMAL(15,2),
    selling_price DECIMAL(15,2),
    export_price DECIMAL(15,4),
    shelf_life_days INTEGER,
    storage_temperature_min DECIMAL(5,2),
    storage_temperature_max DECIMAL(5,2),
    humidity_requirement INTEGER,
    hs_code VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES products_category(id),
    FOREIGN KEY (unit_id) REFERENCES products_unit(id)
);
```

**Dữ liệu mẫu:**
```sql
INSERT INTO products_product VALUES
(1, 'SP-0001', 'Thanh long ruột đỏ', 1, 1, 'Thanh long ruột đỏ xuất khẩu loại A', 'Bình Thuận', 'A', 35000.00, 45000.00, 2.5000, 21, 8.00, 12.00, 85, '0810.90.90', 1, NOW(), NOW()),
(2, 'SP-0002', 'Xoài cát Hòa Lộc', 1, 1, 'Xoài cát Hòa Lộc đặc sản Đồng Tháp', 'Đồng Tháp', 'A', 40000.00, 55000.00, 3.2000, 14, 10.00, 13.00, 90, '0804.50.00', 1, NOW(), NOW()),
(3, 'SP-0003', 'Nhãn lồng Hưng Yên', 1, 1, 'Nhãn lồng tươi xuất khẩu', 'Hưng Yên', 'A', 45000.00, 60000.00, 4.0000, 10, 5.00, 8.00, 90, '0810.20.90', 1, NOW(), NOW());
```

### 6. inventory_warehouse (Kho hàng)
```sql
CREATE TABLE inventory_warehouse (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL,
    address TEXT,
    manager_id BIGINT,
    capacity DECIMAL(10,2),
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (manager_id) REFERENCES accounts_customuser(id)
);
```

**Dữ liệu mẫu:**
```sql
INSERT INTO inventory_warehouse VALUES
(1, 'Kho Trung tâm TP.HCM', 'KHO-HCM', 'Khu Công nghiệp Tân Bình, TP.HCM', 2, 500.00, 1, NOW()),
(2, 'Kho Cần Thơ', 'KHO-CT', 'Khu Công nghiệp Trà Nóc, Cần Thơ', 3, 300.00, 1, NOW());
```

### 7. inventory_inventorystock (Tồn kho)
```sql
CREATE TABLE inventory_inventorystock (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    warehouse_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    quantity DECIMAL(10,2) DEFAULT 0,
    min_stock_level DECIMAL(10,2) DEFAULT 0,
    max_stock_level DECIMAL(10,2) DEFAULT 0,
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (warehouse_id) REFERENCES inventory_warehouse(id),
    FOREIGN KEY (product_id) REFERENCES products_product(id),
    UNIQUE KEY unique_warehouse_product (warehouse_id, product_id)
);
```

**Dữ liệu mẫu:**
```sql
INSERT INTO inventory_inventorystock VALUES
(1, 1, 1, 5000.00, 1000.00, 10000.00, NOW()),
(2, 1, 2, 3000.00, 800.00, 8000.00, NOW()),
(3, 2, 3, 2000.00, 500.00, 5000.00, NOW());
```

### 8. orders_order (Đơn hàng)
```sql
CREATE TABLE orders_order (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    order_number VARCHAR(20) UNIQUE NOT NULL,
    order_type VARCHAR(20) NOT NULL,
    company_id BIGINT NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    payment_status VARCHAR(20) DEFAULT 'pending',
    order_date DATE DEFAULT (CURRENT_DATE),
    delivery_date DATE,
    expected_delivery DATE,
    shipping_address TEXT,
    shipping_contact VARCHAR(255),
    shipping_phone VARCHAR(20),
    subtotal DECIMAL(15,2) DEFAULT 0,
    tax_amount DECIMAL(15,2) DEFAULT 0,
    shipping_cost DECIMAL(15,2) DEFAULT 0,
    total_amount DECIMAL(15,2) DEFAULT 0,
    notes TEXT,
    created_by_id BIGINT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies_company(id),
    FOREIGN KEY (created_by_id) REFERENCES accounts_customuser(id)
);
```

**Dữ liệu mẫu:**
```sql
INSERT INTO orders_order VALUES
(1, 'EX-000001', 'export', 2, 'confirmed', 'pending', CURDATE(), DATE_ADD(CURDATE(), INTERVAL 30 DAY), DATE_ADD(CURDATE(), INTERVAL 30 DAY), 'Port of Los Angeles, CA, USA', 'John Smith', '+1-555-123-4567', 50000.00, 5000.00, 8000.00, 63000.00, 'Đơn hàng xuất khẩu thanh long sang Mỹ', 3, NOW(), NOW());
```

### 9. orders_orderdetail (Chi tiết đơn hàng)
```sql
CREATE TABLE orders_orderdetail (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    order_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    quantity DECIMAL(10,2) NOT NULL,
    unit_price DECIMAL(15,4) NOT NULL,
    total_price DECIMAL(15,2) NOT NULL,
    tax_rate DECIMAL(5,2) DEFAULT 0,
    notes TEXT,
    FOREIGN KEY (order_id) REFERENCES orders_order(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products_product(id)
);
```

**Dữ liệu mẫu:**
```sql
INSERT INTO orders_orderdetail VALUES
(1, 1, 1, 20000.00, 2.5000, 50000.00, 10.00, '');
```

### 10. payments_exchangerate (Tỷ giá)
```sql
CREATE TABLE payments_exchangerate (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    from_currency VARCHAR(3) NOT NULL,
    to_currency VARCHAR(3) NOT NULL,
    rate DECIMAL(15,4) NOT NULL,
    effective_date DATE NOT NULL,
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**Dữ liệu mẫu:**
```sql
INSERT INTO payments_exchangerate VALUES
(1, 'USD', 'VND', 24500.0000, CURDATE(), 'Tỷ giá USD/VND hôm nay', NOW());
```

### 11. news_newscategory (Danh mục tin tức)
```sql
CREATE TABLE news_newscategory (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    color VARCHAR(7) DEFAULT '#007bff'
);
```

**Dữ liệu mẫu:**
```sql
INSERT INTO news_newscategory VALUES
(1, 'Tin nội bộ', 'Thông báo nội bộ công ty', '#007bff'),
(2, 'Thị trường', 'Tin tức thị trường trái cây', '#28a745');
```

### 12. news_news (Tin tức)
```sql
CREATE TABLE news_news (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    summary TEXT,
    content LONGTEXT,
    category_id BIGINT,
    news_type VARCHAR(20) DEFAULT 'internal',
    status VARCHAR(20) DEFAULT 'draft',
    is_featured BOOLEAN DEFAULT FALSE,
    publish_date DATETIME,
    author_id BIGINT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES news_newscategory(id),
    FOREIGN KEY (author_id) REFERENCES accounts_customuser(id)
);
```

**Dữ liệu mẫu:**
```sql
INSERT INTO news_news VALUES
(1, 'Chào mừng đến với hệ thống quản lý xuất nhập khẩu trái cây', 'chao-mung-he-thong', 'Hệ thống mới được triển khai để quản lý toàn bộ quy trình xuất nhập khẩu', '<p>Chúng tôi vui mừng thông báo hệ thống quản lý xuất nhập khẩu trái cây đã chính thức được triển khai...</p>', 1, 'internal', 'published', 1, NOW(), 1, NOW(), NOW()),
(2, 'Thị trường xuất khẩu thanh long sang Mỹ tăng trường mạnh', 'thi-truong-xuat-khau-thanh-long', 'Nhu cầu thanh long Việt Nam tại thị trường Mỹ tăng 15% so với cùng kỳ', '<p>Theo báo cáo mới nhất, xuất khẩu thanh long của Việt Nam sang thị trường Mỹ đạt mức tăng trưởng ấn tượng...</p>', 2, 'market', 'published', 0, NOW(), 2, NOW(), NOW());
```

---

## 📊 Relationships (Mối quan hệ)

### Quan hệ chính:
1. **User (1) → (N) Orders**: Một user tạo nhiều đơn hàng
2. **Company (1) → (N) Orders**: Một công ty có nhiều đơn hàng  
3. **Order (1) → (N) OrderDetails**: Một đơn hàng có nhiều sản phẩm
4. **Product (1) → (N) OrderDetails**: Một sản phẩm trong nhiều đơn hàng
5. **Product (1) → (N) InventoryStock**: Một sản phẩm tồn ở nhiều kho
6. **Warehouse (1) → (N) InventoryStock**: Một kho chứa nhiều sản phẩm
7. **Category (1) → (N) Products**: Một danh mục có nhiều sản phẩm

---

## 🔧 Scripts tạo dữ liệu mẫu

### Script SQL tạo toàn bộ dữ liệu:
```sql
-- Tạo users
INSERT INTO accounts_customuser (username, email, first_name, last_name, phone, role, is_active, is_staff, is_superuser, date_joined, password) VALUES
('admin', 'admin@company.com', 'Admin', 'System', '0909000000', 'admin', 1, 1, 1, NOW(), 'pbkdf2_sha256$...'),
('manager1', 'manager@company.com', 'Nguyễn', 'Quản Lý', '0909123456', 'manager', 1, 0, 0, NOW(), 'pbkdf2_sha256$...'),
('staff1', 'staff@company.com', 'Trần', 'Nhân Viên', '0909123457', 'staff', 1, 0, 0, NOW(), 'pbkdf2_sha256$...');

-- Tạo companies
INSERT INTO companies_company (name, company_type, tax_code, address, phone, email, contact_person, contact_phone, contact_email, export_license, import_license, is_active, created_at, updated_at) VALUES
('Công ty TNHH Xuất Nhập Khẩu Trái Cây Việt Nam', 'our_company', '0123456789', '123 Đường ABC, Quận 1, TP.HCM', '028-12345678', 'info@fruitexport.vn', 'Nguyễn Văn A', '0909123456', 'nguyena@fruitexport.vn', 'XK-001/2023', 'NK-001/2023', 1, NOW(), NOW()),
('Fresh Fruit USA Inc.', 'customer', 'US123456789', '123 Main St, New York, USA', '+1-555-123-4567', 'orders@freshfruit-usa.com', 'John Smith', '+1-555-123-4567', 'john@freshfruit-usa.com', '', '', 1, NOW(), NOW()),
('Hợp tác xã Trái cây Đồng Nai', 'supplier', '9876543210', 'Huyện Long Khánh, Tỉnh Đồng Nai', '0251-123456', 'htx@dongnai-fruit.vn', 'Lê Thị B', '0909876543', 'lethib@dongnai-fruit.vn', '', '', 1, NOW(), NOW());

-- Tạo categories và units
INSERT INTO products_category (name, description, is_active, created_at) VALUES
('Trái cây nhiệt đới', 'Các loại trái cây nhiệt đới xuất khẩu', 1, NOW()),
('Trái cây có múi', 'Cam, quýt, bưởi và các loại có múi', 1, NOW());

INSERT INTO products_unit (name, symbol) VALUES
('Kilogram', 'kg'),
('Tấn', 'tấn'),
('Thùng', 'thùng');

-- Tạo products
INSERT INTO products_product (code, name, category_id, unit_id, description, origin, quality_grade, cost_price, selling_price, export_price, shelf_life_days, storage_temperature_min, storage_temperature_max, humidity_requirement, hs_code, is_active, created_at, updated_at) VALUES
('SP-0001', 'Thanh long ruột đỏ', 1, 1, 'Thanh long ruột đỏ xuất khẩu loại A', 'Bình Thuận', 'A', 35000.00, 45000.00, 2.5000, 21, 8.00, 12.00, 85, '0810.90.90', 1, NOW(), NOW()),
('SP-0002', 'Xoài cát Hòa Lộc', 1, 1, 'Xoài cát Hòa Lộc đặc sản Đồng Tháp', 'Đồng Tháp', 'A', 40000.00, 55000.00, 3.2000, 14, 10.00, 13.00, 90, '0804.50.00', 1, NOW(), NOW()),
('SP-0003', 'Nhãn lồng Hưng Yên', 1, 1, 'Nhãn lồng tươi xuất khẩu', 'Hưng Yên', 'A', 45000.00, 60000.00, 4.0000, 10, 5.00, 8.00, 90, '0810.20.90', 1, NOW(), NOW());

-- Tạo warehouses
INSERT INTO inventory_warehouse (name, code, address, manager_id, capacity, is_active, created_at) VALUES
('Kho Trung tâm TP.HCM', 'KHO-HCM', 'Khu Công nghiệp Tân Bình, TP.HCM', 2, 500.00, 1, NOW()),
('Kho Cần Thơ', 'KHO-CT', 'Khu Công nghiệp Trà Nóc, Cần Thơ', 3, 300.00, 1, NOW());

-- Tạo inventory stocks
INSERT INTO inventory_inventorystock (warehouse_id, product_id, quantity, min_stock_level, max_stock_level, last_updated) VALUES
(1, 1, 5000.00, 1000.00, 10000.00, NOW()),
(1, 2, 3000.00, 800.00, 8000.00, NOW()),
(2, 3, 2000.00, 500.00, 5000.00, NOW());

-- Tạo orders
INSERT INTO orders_order (order_number, order_type, company_id, status, payment_status, order_date, delivery_date, expected_delivery, shipping_address, shipping_contact, shipping_phone, subtotal, tax_amount, shipping_cost, total_amount, notes, created_by_id, created_at, updated_at) VALUES
('EX-000001', 'export', 2, 'confirmed', 'pending', CURDATE(), DATE_ADD(CURDATE(), INTERVAL 30 DAY), DATE_ADD(CURDATE(), INTERVAL 30 DAY), 'Port of Los Angeles, CA, USA', 'John Smith', '+1-555-123-4567', 50000.00, 5000.00, 8000.00, 63000.00, 'Đơn hàng xuất khẩu thanh long sang Mỹ', 3, NOW(), NOW());

-- Tạo order details
INSERT INTO orders_orderdetail (order_id, product_id, quantity, unit_price, total_price, tax_rate, notes) VALUES
(1, 1, 20000.00, 2.5000, 50000.00, 10.00, '');

-- Tạo exchange rates
INSERT INTO payments_exchangerate (from_currency, to_currency, rate, effective_date, notes, created_at) VALUES
('USD', 'VND', 24500.0000, CURDATE(), 'Tỷ giá USD/VND hôm nay', NOW());

-- Tạo news categories và news
INSERT INTO news_newscategory (name, description, color) VALUES
('Tin nội bộ', 'Thông báo nội bộ công ty', '#007bff'),
('Thị trường', 'Tin tức thị trường trái cây', '#28a745');

INSERT INTO news_news (title, slug, summary, content, category_id, news_type, status, is_featured, publish_date, author_id, created_at, updated_at) VALUES
('Chào mừng đến với hệ thống quản lý xuất nhập khẩu trái cây', 'chao-mung-he-thong', 'Hệ thống mới được triển khai để quản lý toàn bộ quy trình xuất nhập khẩu', '<p>Chúng tôi vui mừng thông báo hệ thống quản lý xuất nhập khẩu trái cây đã chính thức được triển khai...</p>', 1, 'internal', 'published', 1, NOW(), 1, NOW(), NOW()),
('Thị trường xuất khẩu thanh long sang Mỹ tăng trường mạnh', 'thi-truong-xuat-khau-thanh-long', 'Nhu cầu thanh long Việt Nam tại thị trường Mỹ tăng 15% so với cùng kỳ', '<p>Theo báo cáo mới nhất, xuất khẩu thanh long của Việt Nam sang thị trường Mỹ đạt mức tăng trưởng ấn tượng...</p>', 2, 'market', 'published', 0, NOW(), 2, NOW(), NOW());
```

---

## 🎯 Các truy vấn hữu ích

### Tìm sản phẩm sắp hết hàng:
```sql
SELECT p.name, w.name as warehouse, s.quantity, s.min_stock_level
FROM inventory_inventorystock s
JOIN products_product p ON s.product_id = p.id
JOIN inventory_warehouse w ON s.warehouse_id = w.id
WHERE s.quantity <= s.min_stock_level;
```

### Thống kê đơn hàng theo tháng:
```sql
SELECT 
    MONTH(created_at) as month,
    order_type,
    COUNT(*) as total_orders,
    SUM(total_amount) as total_value
FROM orders_order 
WHERE YEAR(created_at) = YEAR(NOW())
GROUP BY MONTH(created_at), order_type
ORDER BY month;
```

### Top khách hàng theo doanh số:
```sql
SELECT 
    c.name,
    COUNT(o.id) as total_orders,
    SUM(o.total_amount) as total_amount
FROM companies_company c
JOIN orders_order o ON c.id = o.company_id
WHERE c.company_type = 'customer'
GROUP BY c.id, c.name
ORDER BY total_amount DESC
LIMIT 10;
```

*Schema này được cập nhật theo phiên bản Django hiện tại. Các foreign key và constraint được Django ORM quản lý tự động.*
