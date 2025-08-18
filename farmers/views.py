from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Avg, Count
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Farmer, FarmingArea, CropProduct, FarmerDocument
from .forms import FarmerForm, FarmerUpdateForm

# Class-based views
class FarmerListView(LoginRequiredMixin, ListView):
    """Danh sách trang trại"""
    model = Farmer
    template_name = 'farmers/list.html'
    context_object_name = 'farmers'
    paginate_by = 20
    
    def get_queryset(self):
        return Farmer.objects.filter(is_active=True).order_by('-created_at')

class FarmerDetailView(LoginRequiredMixin, DetailView):
    """Chi tiết trang trại"""
    model = Farmer
    template_name = 'farmers/detail.html'
    context_object_name = 'farmer'

class FarmerCreateView(LoginRequiredMixin, CreateView):
    """Tạo trang trại mới"""
    model = Farmer
    form_class = FarmerForm
    template_name = 'farmers/create.html'
    success_url = reverse_lazy('farmers:list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Trang trại đã được tạo thành công!')
        return super().form_valid(form)

class FarmerUpdateView(LoginRequiredMixin, UpdateView):
    """Cập nhật trang trại"""
    model = Farmer
    form_class = FarmerUpdateForm
    template_name = 'farmers/update.html'
    success_url = reverse_lazy('farmers:list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Thông tin trang trại đã được cập nhật!')
        return super().form_valid(form)

class FarmerDeleteView(LoginRequiredMixin, DeleteView):
    """Xóa trang trại"""
    model = Farmer
    template_name = 'farmers/delete.html'
    success_url = reverse_lazy('farmers:list')

# Function-based views (cũ)
@login_required
def farmer_list(request):
    """Danh sách nông dân với thông tin sản phẩm"""
    farmers = Farmer.objects.annotate(
        product_count=Count('crop_products'),
        avg_rating=Avg('customer_reviews__rating')
    ).select_related().prefetch_related('crop_products')
    
    # Tìm kiếm
    search = request.GET.get('search')
    if search:
        farmers = farmers.filter(
            Q(farmer_code__icontains=search) |
            Q(name__icontains=search) |
            Q(phone__icontains=search) |
            Q(email__icontains=search) |
            Q(farming_region__icontains=search) |
            Q(main_crops__icontains=search)
        )
    
    # Lọc theo loại hình
    farmer_type = request.GET.get('farmer_type')
    if farmer_type:
        farmers = farmers.filter(farmer_type=farmer_type)
    
    # Lọc theo chứng nhận
    certification = request.GET.get('certification')
    if certification:
        farmers = farmers.filter(certifications=certification)
    
    # Lọc theo trạng thái
    is_active = request.GET.get('is_active')
    if is_active:
        farmers = farmers.filter(is_active=is_active == 'true')
        
    is_verified = request.GET.get('is_verified')
    if is_verified:
        farmers = farmers.filter(is_verified=is_verified == 'true')
        
    # Sắp xếp
    sort_by = request.GET.get('sort_by', '-created_at')
    if sort_by in ['name', '-name', 'rating', '-rating', 'product_count', '-product_count', 'created_at', '-created_at']:
        farmers = farmers.order_by(sort_by)
        
    # Phân trang
    paginator = Paginator(farmers, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'farmer_type_choices': Farmer.FARMER_TYPE_CHOICES,
        'certification_choices': Farmer.CERTIFICATION_CHOICES,
        'search': search,
        'farmer_type': farmer_type,
        'certification': certification,
        'is_active': is_active,
        'is_verified': is_verified,
        'sort_by': sort_by,
    }
    return render(request, 'farmers/farmer_list.html', context)

@login_required
def farmer_detail(request, farmer_id):
    """Chi tiết nông dân với thông tin canh tác và sản phẩm"""
    farmer = get_object_or_404(Farmer, id=farmer_id)
    farming_areas = farmer.farming_areas.all()
    products = farmer.crop_products.select_related('farming_area').order_by('-created_at')
    documents = farmer.documents.all()
    reviews = farmer.customer_reviews.select_related('customer').order_by('-created_at')[:10]
    
    # Thống kê
    total_products = products.count()
    available_products = products.filter(is_available=True).count()
    avg_rating = reviews.aggregate(avg=Avg('rating'))['avg'] or 0
    
    context = {
        'farmer': farmer,
        'farming_areas': farming_areas,
        'products': products,
        'documents': documents,
        'reviews': reviews,
        'stats': {
            'total_products': total_products,
            'available_products': available_products,
            'avg_rating': round(avg_rating, 2) if avg_rating else 0,
            'total_reviews': reviews.count(),
        }
    }
    return render(request, 'farmers/farmer_detail.html', context)

@login_required
def farmer_products(request, farmer_id):
    """Danh sách sản phẩm của nông dân"""
    farmer = get_object_or_404(Farmer, id=farmer_id)
    products = farmer.crop_products.select_related('farming_area')
    
    # Lọc theo mùa vụ
    season = request.GET.get('season')
    if season:
        products = products.filter(harvest_season=season)
    
    # Lọc theo chất lượng
    quality = request.GET.get('quality')
    if quality:
        products = products.filter(quality_grade=quality)
        
    # Lọc theo trạng thái
    is_available = request.GET.get('is_available')
    if is_available:
        products = products.filter(is_available=is_available == 'true')
        
    is_organic = request.GET.get('is_organic')
    if is_organic:
        products = products.filter(is_organic=is_organic == 'true')
    
    # Sắp xếp
    sort_by = request.GET.get('sort_by', '-created_at')
    if sort_by in ['product_name', '-product_name', 'price_per_kg', '-price_per_kg', 
                   'expected_harvest_date', '-expected_harvest_date', 'created_at', '-created_at']:
        products = products.order_by(sort_by)
    
    # Phân trang
    paginator = Paginator(products, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'farmer': farmer,
        'page_obj': page_obj,
        'season_choices': CropProduct.SEASON_CHOICES,
        'quality_choices': CropProduct.QUALITY_GRADE_CHOICES,
        'season': season,
        'quality': quality,
        'is_available': is_available,
        'is_organic': is_organic,
        'sort_by': sort_by,
    }
    return render(request, 'farmers/farmer_products.html', context)

@login_required
def farmer_farming_areas(request, farmer_id):
    """Khu vực canh tác của nông dân"""
    farmer = get_object_or_404(Farmer, id=farmer_id)
    farming_areas = farmer.farming_areas.prefetch_related('products').all()
    
    context = {
        'farmer': farmer,
        'farming_areas': farming_areas,
    }
    return render(request, 'farmers/farmer_farming_areas.html', context)

@login_required
def farmer_add(request):
    """Thêm nông dân mới"""
    if request.method == 'POST':
        # TODO: Implement form processing
        # Tạo form để xử lý thêm nông dân
        messages.success(request, 'Thêm nông dân thành công!')
        return redirect('farmers:farmer_list')
    
    context = {
        'farmer_type_choices': Farmer.FARMER_TYPE_CHOICES,
        'certification_choices': Farmer.CERTIFICATION_CHOICES,
    }
    return render(request, 'farmers/farmer_add.html', context)

@login_required
def farmer_edit(request, farmer_id):
    """Chỉnh sửa thông tin nông dân"""
    farmer = get_object_or_404(Farmer, id=farmer_id)
    
    if request.method == 'POST':
        # TODO: Implement form processing
        # Cập nhật thông tin nông dân
        messages.success(request, f'Cập nhật thông tin {farmer.name} thành công!')
        return redirect('farmers:farmer_detail', farmer_id=farmer.id)
    
    context = {
        'farmer': farmer,
        'farmer_type_choices': Farmer.FARMER_TYPE_CHOICES,
        'certification_choices': Farmer.CERTIFICATION_CHOICES,
    }
    return render(request, 'farmers/farmer_edit.html', context)

@login_required
def farmer_delete(request, farmer_id):
    """Xóa nông dân"""
    farmer = get_object_or_404(Farmer, id=farmer_id)
    
    if request.method == 'POST':
        farmer_name = farmer.name
        farmer.delete()
        messages.success(request, f'Đã xóa nông dân {farmer_name}')
        return redirect('farmers:farmer_list')
    
    context = {'farmer': farmer}
    return render(request, 'farmers/farmer_delete.html', context)

@login_required
def farmer_documents(request, farmer_id):
    """Tài liệu của nông dân"""
    farmer = get_object_or_404(Farmer, id=farmer_id)
    documents = farmer.documents.all().order_by('-uploaded_at')
    
    context = {
        'farmer': farmer,
        'documents': documents,
    }
    return render(request, 'farmers/farmer_documents.html', context)

@login_required
def product_detail(request, product_id):
    """Chi tiết sản phẩm nông nghiệp"""
    product = get_object_or_404(CropProduct, id=product_id)
    farmer = product.farmer
    
    # Sản phẩm khác của nông dân
    other_products = farmer.crop_products.exclude(id=product_id).filter(is_available=True)[:5]
    
    context = {
        'product': product,
        'farmer': farmer,
        'other_products': other_products,
    }
    return render(request, 'farmers/product_detail.html', context)

@login_required
def search_products(request):
    """Tìm kiếm sản phẩm nông nghiệp"""
    products = CropProduct.objects.select_related('farmer', 'farming_area').filter(is_available=True)
    
    # Tìm kiếm theo tên
    search = request.GET.get('search')
    if search:
        products = products.filter(
            Q(product_name__icontains=search) |
            Q(variety__icontains=search) |
            Q(farmer__name__icontains=search) |
            Q(farmer__farming_region__icontains=search)
        )
    
    # Lọc theo mùa vụ
    season = request.GET.get('season')
    if season:
        products = products.filter(harvest_season=season)
    
    # Lọc theo chất lượng
    quality = request.GET.get('quality')
    if quality:
        products = products.filter(quality_grade=quality)
        
    # Lọc theo giá
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price_per_kg__gte=min_price)
    if max_price:
        products = products.filter(price_per_kg__lte=max_price)
        
    # Lọc sản phẩm hữu cơ
    is_organic = request.GET.get('is_organic')
    if is_organic == 'true':
        products = products.filter(is_organic=True)
    
    # Sắp xếp
    sort_by = request.GET.get('sort_by', '-created_at')
    if sort_by in ['product_name', '-product_name', 'price_per_kg', '-price_per_kg', 
                   'expected_harvest_date', '-expected_harvest_date']:
        products = products.order_by(sort_by)
    
    # Phân trang
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'season_choices': CropProduct.SEASON_CHOICES,
        'quality_choices': CropProduct.QUALITY_GRADE_CHOICES,
        'search': search,
        'season': season,
        'quality': quality,
        'min_price': min_price,
        'max_price': max_price,
        'is_organic': is_organic,
        'sort_by': sort_by,
    }
    return render(request, 'farmers/search_products.html', context)
