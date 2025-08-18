#!/usr/bin/env python
"""
Script tạo dữ liệu mẫu cho hệ thống quản lý xuất nhập khẩu trái cây
Chạy bằng lệnh: python manage.py shell < scripts/create_sample_data.py
"""

import os
import sys
import django
from datetime import datetime, date, timedelta
from decimal import Decimal

# Setup Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fruit_manage.settings')
django.setup()

from django.contrib.auth import get_user_model
from companies.models import Company, CompanyDocument
from products.models import Category, Unit, Product
from inventory.models import Warehouse, InventoryStock
from orders.models import Order, OrderDetail
from payments.models import Payment, ExchangeRate
from news.models import NewsCategory, News

User = get_user_model()

def create_sample_data():
    print("Bắt đầu tạo dữ liệu mẫu...")
    
    # 1. Tạo users
    print("Tạo users...")
    admin_user = User.objects.filter(username='admin').first()
    if not admin_user:
        admin_user = User.objects.create_user(
            username='admin',
            email='admin@company.com',
            password='admin123',
            first_name='Admin',
            last_name='System',
            role='admin',
            is_staff=True,
            is_superuser=True
        )
    
    manager = User.objects.create_user(
        username='manager1',
        email='manager@company.com',
        password='manager123',
        first_name='Nguyễn',
        last_name='Quản Lý',
        role='manager',
        phone='0909123456'
    )
    
    staff = User.objects.create_user(
        username='staff1',
        email='staff@company.com',
        password='staff123',
        first_name='Trần',
        last_name='Nhân Viên',
        role='staff',
        phone='0909123457'
    )
    
    # 2. Tạo companies
    print("Tạo companies...")
    our_company = Company.objects.create(
        name='Công ty TNHH Xuất Nhập Khẩu Trái Cây Việt Nam',
        company_type='our_company',
        tax_code='0123456789',
        address='123 Đường ABC, Quận 1, TP.HCM',
        phone='028-12345678',
        email='info@fruitexport.vn',
        contact_person='Nguyễn Văn A',
        contact_phone='0909123456',
        contact_email='nguyena@fruitexport.vn',
        export_license='XK-001/2023',
        import_license='NK-001/2023'
    )
    
    us_customer = Company.objects.create(
        name='Fresh Fruit USA Inc.',
        company_type='customer',
        tax_code='US123456789',
        address='123 Main St, New York, USA',
        phone='+1-555-123-4567',
        email='orders@freshfruit-usa.com',
        contact_person='John Smith',
        contact_phone='+1-555-123-4567',
        contact_email='john@freshfruit-usa.com'
    )
    
    supplier = Company.objects.create(
        name='Hợp tác xã Trái cây Đồng Nai',
        company_type='supplier',
        tax_code='9876543210',
        address='Huyện Long Khánh, Tỉnh Đồng Nai',
        phone='0251-123456',
        email='htx@dongnai-fruit.vn',
        contact_person='Lê Thị B',
        contact_phone='0909876543',
        contact_email='lethib@dongnai-fruit.vn'
    )
    
    # 3. Tạo categories và units
    print("Tạo categories và units...")
    cat_tropical = Category.objects.create(
        name='Trái cây nhiệt đới',
        description='Các loại trái cây nhiệt đới xuất khẩu'
    )
    
    cat_citrus = Category.objects.create(
        name='Trái cây có múi',
        description='Cam, quýt, bưởi và các loại có múi'
    )
    
    unit_kg = Unit.objects.create(name='Kilogram', symbol='kg')
    unit_ton = Unit.objects.create(name='Tấn', symbol='tấn')
    unit_box = Unit.objects.create(name='Thùng', symbol='thùng')
    
    # 4. Tạo products
    print("Tạo products...")
    dragon_fruit = Product.objects.create(
        code='SP-0001',
        name='Thanh long ruột đỏ',
        category=cat_tropical,
        unit=unit_kg,
        description='Thanh long ruột đỏ xuất khẩu loại A',
        origin='Bình Thuận',
        quality_grade='A',
        cost_price=Decimal('35000'),
        selling_price=Decimal('45000'),
        export_price=Decimal('2.50'),  # USD per kg
        shelf_life_days=21,
        storage_temperature_min=Decimal('8'),
        storage_temperature_max=Decimal('12'),
        humidity_requirement=85,
        hs_code='0810.90.90'
    )
    
    mango = Product.objects.create(
        code='SP-0002',
        name='Xoài cát Hòa Lộc',
        category=cat_tropical,
        unit=unit_kg,
        description='Xoài cát Hòa Lộc đặc sản Đồng Tháp',
        origin='Đồng Tháp',
        quality_grade='A',
        cost_price=Decimal('40000'),
        selling_price=Decimal('55000'),
        export_price=Decimal('3.20'),
        shelf_life_days=14,
        storage_temperature_min=Decimal('10'),
        storage_temperature_max=Decimal('13'),
        humidity_requirement=90,
        hs_code='0804.50.00'
    )
    
    longan = Product.objects.create(
        code='SP-0003',
        name='Nhãn lồng Hưng Yên',
        category=cat_tropical,
        unit=unit_kg,
        description='Nhãn lồng tươi xuất khẩu',
        origin='Hưng Yên',
        quality_grade='A',
        cost_price=Decimal('45000'),
        selling_price=Decimal('60000'),
        export_price=Decimal('4.00'),
        shelf_life_days=10,
        storage_temperature_min=Decimal('5'),
        storage_temperature_max=Decimal('8'),
        humidity_requirement=90,
        hs_code='0810.20.90'
    )
    
    # 5. Tạo warehouses
    print("Tạo warehouses...")
    warehouse_hcm = Warehouse.objects.create(
        name='Kho Trung tâm TP.HCM',
        code='KHO-HCM',
        address='Khu Công nghiệp Tân Bình, TP.HCM',
        manager=manager,
        capacity=Decimal('500.00')
    )
    
    warehouse_can_tho = Warehouse.objects.create(
        name='Kho Cần Thơ',
        code='KHO-CT',
        address='Khu Công nghiệp Trà Nóc, Cần Thơ',
        manager=staff,
        capacity=Decimal('300.00')
    )
    
    # 6. Tạo inventory stocks
    print("Tạo inventory stocks...")
    InventoryStock.objects.create(
        warehouse=warehouse_hcm,
        product=dragon_fruit,
        quantity=Decimal('5000'),
        min_stock_level=Decimal('1000'),
        max_stock_level=Decimal('10000')
    )
    
    InventoryStock.objects.create(
        warehouse=warehouse_hcm,
        product=mango,
        quantity=Decimal('3000'),
        min_stock_level=Decimal('800'),
        max_stock_level=Decimal('8000')
    )
    
    InventoryStock.objects.create(
        warehouse=warehouse_can_tho,
        product=longan,
        quantity=Decimal('2000'),
        min_stock_level=Decimal('500'),
        max_stock_level=Decimal('5000')
    )
    
    # 7. Tạo orders
    print("Tạo orders...")
    export_order = Order.objects.create(
        order_number='EX-000001',
        order_type='export',
        company=us_customer,
        status='confirmed',
        payment_status='pending',
        delivery_date=date.today() + timedelta(days=30),
        expected_delivery=date.today() + timedelta(days=30),
        shipping_address='Port of Los Angeles, CA, USA',
        shipping_contact='John Smith',
        shipping_phone='+1-555-123-4567',
        subtotal=Decimal('50000.00'),
        tax_amount=Decimal('5000.00'),
        shipping_cost=Decimal('8000.00'),
        total_amount=Decimal('63000.00'),
        notes='Đơn hàng xuất khẩu thanh long sang Mỹ',
        created_by=staff
    )
    
    # 8. Tạo order details
    OrderDetail.objects.create(
        order=export_order,
        product=dragon_fruit,
        quantity=Decimal('20000'),  # 20 tấn
        unit_price=Decimal('2.50'),
        total_price=Decimal('50000.00'),
        tax_rate=Decimal('10.00')
    )
    
    # 9. Tạo exchange rates
    print("Tạo exchange rates...")
    ExchangeRate.objects.create(
        from_currency='USD',
        to_currency='VND',
        rate=Decimal('24500.0000'),
        effective_date=date.today(),
        notes='Tỷ giá USD/VND hôm nay'
    )
    
    # 10. Tạo news categories và news
    print("Tạo news...")
    news_cat_internal = NewsCategory.objects.create(
        name='Tin nội bộ',
        description='Thông báo nội bộ công ty',
        color='#007bff'
    )
    
    news_cat_market = NewsCategory.objects.create(
        name='Thị trường',
        description='Tin tức thị trường trái cây',
        color='#28a745'
    )
    
    News.objects.create(
        title='Chào mừng đến với hệ thống quản lý xuất nhập khẩu trái cây',
        slug='chao-mung-he-thong',
        summary='Hệ thống mới được triển khai để quản lý toàn bộ quy trình xuất nhập khẩu',
        content='<p>Chúng tôi vui mừng thông báo hệ thống quản lý xuất nhập khẩu trái cây đã chính thức được triển khai...</p>',
        category=news_cat_internal,
        news_type='internal',
        status='published',
        is_featured=True,
        publish_date=datetime.now(),
        author=admin_user
    )
    
    News.objects.create(
        title='Thị trường xuất khẩu thanh long sang Mỹ tăng trường mạnh',
        slug='thi-truong-xuat-khau-thanh-long',
        summary='Nhu cầu thanh long Việt Nam tại thị trường Mỹ tăng 15% so với cùng kỳ',
        content='<p>Theo báo cáo mới nhất, xuất khẩu thanh long của Việt Nam sang thị trường Mỹ đạt mức tăng trưởng ấn tượng...</p>',
        category=news_cat_market,
        news_type='market',
        status='published',
        publish_date=datetime.now(),
        author=manager
    )
    
    print("✅ Tạo dữ liệu mẫu thành công!")
    print(f"- Đã tạo {User.objects.count()} users")
    print(f"- Đã tạo {Company.objects.count()} companies")
    print(f"- Đã tạo {Product.objects.count()} products")
    print(f"- Đã tạo {Order.objects.count()} orders")
    print(f"- Đã tạo {News.objects.count()} news")

if __name__ == '__main__':
    create_sample_data()
