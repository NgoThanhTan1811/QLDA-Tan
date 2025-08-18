from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count, Q, F
from django.utils import timezone
from datetime import datetime, timedelta
from django.http import JsonResponse

from orders.models import Order, OrderDetail
from products.models import Product
from farmers.models import Farmer
from customers.models import Customer
from inventory.models import InventoryStock
from payments.models import Payment

class DashboardHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Thống kê tổng quan
        context['total_orders'] = Order.objects.count()
        context['total_products'] = Product.objects.filter(is_active=True).count()
        context['total_farmers'] = Farmer.objects.filter(is_active=True).count()
        context['total_customers'] = Customer.objects.filter(is_active=True).count()
        context['total_revenue'] = Order.objects.filter(
            status='completed'
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        
        # Đơn hàng gần đây
        context['recent_orders'] = Order.objects.select_related(
            'farmer', 'customer', 'created_by'
        ).order_by('-created_at')[:10]
        
        # Sản phẩm tồn kho thấp
        context['low_stock_products'] = InventoryStock.objects.select_related(
            'product', 'warehouse'
        ).filter(
            quantity__lte=F('min_stock_level')
        )[:10]
        
        # Thanh toán chờ xử lý
        context['pending_payments'] = Payment.objects.filter(
            status='pending'
        ).select_related('order', 'farmer', 'customer')[:10]
        
        return context

class DashboardStatsView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/stats.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Thống kê theo tháng
        today = timezone.now().date()
        current_month = today.replace(day=1)
        last_month = (current_month - timedelta(days=1)).replace(day=1)
        
        # Đơn hàng trong tháng
        current_month_orders = Order.objects.filter(
            created_at__date__gte=current_month
        ).count()
        
        last_month_orders = Order.objects.filter(
            created_at__date__gte=last_month,
            created_at__date__lt=current_month
        ).count()
        
        context['current_month_orders'] = current_month_orders
        context['last_month_orders'] = last_month_orders
        
        # Doanh thu trong tháng
        current_month_revenue = Order.objects.filter(
            created_at__date__gte=current_month,
            status='completed'
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        
        last_month_revenue = Order.objects.filter(
            created_at__date__gte=last_month,
            created_at__date__lt=current_month,
            status='completed'
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        
        context['current_month_revenue'] = current_month_revenue
        context['last_month_revenue'] = last_month_revenue
        
        # Thống kê theo loại đơn hàng
        order_type_stats = Order.objects.values('order_type').annotate(
            count=Count('id'),
            total_amount=Sum('total_amount')
        ).order_by('-count')
        
        context['order_type_stats'] = order_type_stats
        
        return context

class DashboardChartsView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        chart_type = request.GET.get('type', 'revenue')
        
        if chart_type == 'revenue':
            return self.get_revenue_chart_data()
        elif chart_type == 'orders':
            return self.get_orders_chart_data()
        elif chart_type == 'products':
            return self.get_products_chart_data()
        
        return JsonResponse({'error': 'Invalid chart type'})
    
    def get_revenue_chart_data(self):
        # Doanh thu 12 tháng gần nhất
        today = timezone.now().date()
        months = []
        revenues = []
        
        for i in range(12):
            month_date = today.replace(day=1) - timedelta(days=30*i)
            next_month = (month_date.replace(day=28) + timedelta(days=4)).replace(day=1)
            
            revenue = Order.objects.filter(
                created_at__date__gte=month_date,
                created_at__date__lt=next_month,
                status='completed'
            ).aggregate(total=Sum('total_amount'))['total'] or 0
            
            months.insert(0, month_date.strftime('%m/%Y'))
            revenues.insert(0, float(revenue))
        
        return JsonResponse({
            'labels': months,
            'data': revenues
        })
    
    def get_orders_chart_data(self):
        # Số lượng đơn hàng theo trạng thái
        statuses = Order.objects.values('status').annotate(
            count=Count('id')
        ).order_by('-count')
        
        return JsonResponse({
            'labels': [s['status'] for s in statuses],
            'data': [s['count'] for s in statuses]
        })
    
    def get_products_chart_data(self):
        # Top 10 sản phẩm bán chạy
        top_products = OrderDetail.objects.select_related('product').values(
            'product__name'
        ).annotate(
            total_quantity=Sum('quantity')
        ).order_by('-total_quantity')[:10]
        
        return JsonResponse({
            'labels': [p['product__name'] for p in top_products],
            'data': [float(p['total_quantity']) for p in top_products]
        })
