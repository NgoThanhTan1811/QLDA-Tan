from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count, Avg
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Customer, CustomerAddress, CustomerReview, CustomerWishlist, CustomerDocument
from .forms import CustomerForm, CustomerUpdateForm

# Class-based views
class CustomerListView(LoginRequiredMixin, ListView):
    """Danh sách khách hàng"""
    model = Customer
    template_name = 'customers/list.html'
    context_object_name = 'customers'
    paginate_by = 20
    
    def get_queryset(self):
        return Customer.objects.filter(is_active=True).order_by('-created_at')

class CustomerDetailView(LoginRequiredMixin, DetailView):
    """Chi tiết khách hàng"""
    model = Customer
    template_name = 'customers/detail.html'
    context_object_name = 'customer'

class CustomerCreateView(LoginRequiredMixin, CreateView):
    """Tạo khách hàng mới"""
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/create.html'
    success_url = reverse_lazy('customers:list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Khách hàng đã được tạo thành công!')
        return super().form_valid(form)

class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    """Cập nhật khách hàng"""
    model = Customer
    form_class = CustomerUpdateForm
    template_name = 'customers/update.html'
    success_url = reverse_lazy('customers:list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Thông tin khách hàng đã được cập nhật!')
        return super().form_valid(form)

class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    """Xóa khách hàng"""
    model = Customer
    template_name = 'customers/delete.html'
    success_url = reverse_lazy('customers:list')

# Function-based views (cũ)
@login_required
def customer_list(request):
    """Danh sách khách hàng với thống kê"""
    customers = Customer.objects.annotate(
        order_count=Count('orders'),
        review_count=Count('reviews')
    ).select_related('user')
    
    # Tìm kiếm
    search = request.GET.get('search')
    if search:
        customers = customers.filter(
            Q(customer_code__icontains=search) |
            Q(full_name__icontains=search) |
            Q(phone__icontains=search) |
            Q(email__icontains=search) |
            Q(company_name__icontains=search)
        )
    
    # Lọc theo loại khách hàng
    customer_type = request.GET.get('customer_type')
    if customer_type:
        customers = customers.filter(customer_type=customer_type)
    
    # Lọc theo cấp thành viên
    membership = request.GET.get('membership')
    if membership:
        customers = customers.filter(membership_level=membership)
        
    # Lọc theo trạng thái
    is_active = request.GET.get('is_active')
    if is_active:
        customers = customers.filter(is_active=is_active == 'true')
        
    is_vip = request.GET.get('is_vip')
    if is_vip:
        customers = customers.filter(is_vip=is_vip == 'true')
    
    # Sắp xếp
    sort_by = request.GET.get('sort_by', '-created_at')
    if sort_by in ['full_name', '-full_name', 'total_spent', '-total_spent', 
                   'order_count', '-order_count', 'created_at', '-created_at']:
        customers = customers.order_by(sort_by)
        
    # Phân trang
    paginator = Paginator(customers, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'customer_type_choices': Customer.CUSTOMER_TYPE_CHOICES,
        'membership_choices': Customer.MEMBERSHIP_CHOICES,
        'search': search,
        'customer_type': customer_type,
        'membership': membership,
        'is_active': is_active,
        'is_vip': is_vip,
        'sort_by': sort_by,
    }
    return render(request, 'customers/customer_list.html', context)

@login_required
def customer_detail(request, customer_id):
    """Chi tiết khách hàng với thông tin mua sắm"""
    customer = get_object_or_404(Customer, id=customer_id)
    addresses = customer.addresses.all()
    documents = customer.documents.all()
    reviews = customer.reviews.select_related('farmer').order_by('-created_at')[:10]
    wishlist = customer.wishlist.select_related('farmer', 'product')[:10]
    
    # Đơn hàng gần đây
    recent_orders = customer.orders.select_related('farmer').order_by('-created_at')[:5]
    
    # Thống kê
    total_reviews = reviews.count()
    avg_rating_given = reviews.aggregate(avg=Avg('rating'))['avg'] or 0
    
    context = {
        'customer': customer,
        'addresses': addresses,
        'documents': documents,
        'reviews': reviews,
        'wishlist': wishlist,
        'recent_orders': recent_orders,
        'stats': {
            'total_reviews': total_reviews,
            'avg_rating_given': round(avg_rating_given, 2) if avg_rating_given else 0,
            'wishlist_count': wishlist.count(),
        }
    }
    return render(request, 'customers/customer_detail.html', context)

@login_required
def customer_orders(request, customer_id):
    """Đơn hàng của khách hàng"""
    customer = get_object_or_404(Customer, id=customer_id)
    orders = customer.orders.select_related('farmer').order_by('-created_at')
    
    # Lọc theo trạng thái
    status = request.GET.get('status')
    if status:
        orders = orders.filter(status=status)
        
    # Lọc theo thời gian
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')
    if from_date:
        orders = orders.filter(created_at__gte=from_date)
    if to_date:
        orders = orders.filter(created_at__lte=to_date)
    
    # Phân trang
    paginator = Paginator(orders, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'customer': customer,
        'page_obj': page_obj,
        'status': status,
        'from_date': from_date,
        'to_date': to_date,
    }
    return render(request, 'customers/customer_orders.html', context)

@login_required
def customer_reviews(request, customer_id):
    """Đánh giá của khách hàng"""
    customer = get_object_or_404(Customer, id=customer_id)
    reviews = customer.reviews.select_related('farmer', 'order').order_by('-created_at')
    
    # Lọc theo đánh giá
    rating = request.GET.get('rating')
    if rating:
        reviews = reviews.filter(rating=rating)
    
    # Phân trang
    paginator = Paginator(reviews, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'customer': customer,
        'page_obj': page_obj,
        'rating': rating,
    }
    return render(request, 'customers/customer_reviews.html', context)

@login_required
def customer_wishlist(request, customer_id):
    """Danh sách yêu thích của khách hàng"""
    customer = get_object_or_404(Customer, id=customer_id)
    wishlist = customer.wishlist.select_related('farmer', 'product').order_by('-created_at')
    
    context = {
        'customer': customer,
        'wishlist': wishlist,
    }
    return render(request, 'customers/customer_wishlist.html', context)

@login_required
def customer_add(request):
    """Thêm khách hàng mới"""
    if request.method == 'POST':
        # TODO: Implement form processing
        # Tạo form để xử lý thêm khách hàng
        messages.success(request, 'Thêm khách hàng thành công!')
        return redirect('customers:customer_list')
    
    context = {
        'customer_type_choices': Customer.CUSTOMER_TYPE_CHOICES,
        'membership_choices': Customer.MEMBERSHIP_CHOICES,
    }
    return render(request, 'customers/customer_add.html', context)

@login_required
def customer_edit(request, customer_id):
    """Chỉnh sửa thông tin khách hàng"""
    customer = get_object_or_404(Customer, id=customer_id)
    
    if request.method == 'POST':
        # TODO: Implement form processing
        # Cập nhật thông tin khách hàng
        messages.success(request, f'Cập nhật thông tin {customer.full_name} thành công!')
        return redirect('customers:customer_detail', customer_id=customer.id)
    
    context = {
        'customer': customer,
        'customer_type_choices': Customer.CUSTOMER_TYPE_CHOICES,
        'membership_choices': Customer.MEMBERSHIP_CHOICES,
    }
    return render(request, 'customers/customer_edit.html', context)

@login_required
def customer_delete(request, customer_id):
    """Xóa khách hàng"""
    customer = get_object_or_404(Customer, id=customer_id)
    
    if request.method == 'POST':
        customer_name = customer.full_name
        customer.delete()
        messages.success(request, f'Đã xóa khách hàng {customer_name}')
        return redirect('customers:customer_list')
    
    context = {'customer': customer}
    return render(request, 'customers/customer_delete.html', context)

@login_required
def customer_documents(request, customer_id):
    """Tài liệu của khách hàng"""
    customer = get_object_or_404(Customer, id=customer_id)
    documents = customer.documents.all().order_by('-uploaded_at')
    
    context = {
        'customer': customer,
        'documents': documents,
    }
    return render(request, 'customers/customer_documents.html', context)

@login_required
def customer_statistics(request):
    """Thống kê khách hàng"""
    # Thống kê tổng quan
    total_customers = Customer.objects.count()
    active_customers = Customer.objects.filter(is_active=True).count()
    vip_customers = Customer.objects.filter(is_vip=True).count()
    
    # Thống kê theo loại
    customer_type_stats = Customer.objects.values('customer_type').annotate(
        count=Count('id'),
        total_spent=Sum('total_spent')
    ).order_by('-count')
    
    # Thống kê theo cấp thành viên
    membership_stats = Customer.objects.values('membership_level').annotate(
        count=Count('id'),
        total_spent=Sum('total_spent')
    ).order_by('-count')
    
    # Top khách hàng theo chi tiêu
    top_customers = Customer.objects.order_by('-total_spent')[:10]
    
    context = {
        'total_customers': total_customers,
        'active_customers': active_customers,
        'vip_customers': vip_customers,
        'customer_type_stats': customer_type_stats,
        'membership_stats': membership_stats,
        'top_customers': top_customers,
    }
    return render(request, 'customers/customer_statistics.html', context)
