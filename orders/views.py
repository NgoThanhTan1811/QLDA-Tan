from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db import transaction, models
from django.db.models import Q
from django.urls import reverse_lazy
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from .models import Order, OrderDetail
from farmers.models import Farmer
from customers.models import Customer
from products.models import Product

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    paginate_by = 10  # 10 items per page
    
    def get_queryset(self):
        queryset = Order.objects.select_related('farmer', 'customer', 'created_by').all()
        
        # Filter by order type
        order_type = self.request.GET.get('order_type')
        if order_type in ['export', 'import']:
            queryset = queryset.filter(order_type=order_type)
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Search filter
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(order_code__icontains=search) |
                Q(farmer__farm_name__icontains=search) |
                Q(customer__full_name__icontains=search) |
                Q(notes__icontains=search)
            )
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = timezone.now().date()
        return context

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/detail.html'
    context_object_name = 'order'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_details'] = OrderDetail.objects.filter(order=self.object).select_related('product')
        return context

class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    template_name = 'orders/order_create.html'
    fields = ['order_type', 'farmer', 'customer', 'delivery_date', 'shipping_address', 'notes', 'payment_status']
    success_url = reverse_lazy('orders:list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['farmers'] = Farmer.objects.filter(is_active=True)
        context['customers'] = Customer.objects.filter(is_active=True)
        
        # Get products with stock information
        products_list = []
        try:
            from inventory.models import InventoryStock
            from django.db.models import Sum
            
            products = Product.objects.select_related('unit').filter(is_active=True)
            for product in products:
                # Get total stock across all warehouses
                total_stock = InventoryStock.objects.filter(
                    product=product
                ).aggregate(
                    total=Sum('quantity')
                )['total'] or 0
                
                products_list.append({
                    'id': product.id,
                    'name': product.name,
                    'code': product.code,
                    'price': float(product.selling_price),
                    'unit': product.unit.name if product.unit else '',
                    'stock': float(total_stock)
                })
        except ImportError:
            # Fallback if inventory module is not available
            products = Product.objects.select_related('unit').filter(is_active=True)
            for product in products:
                products_list.append({
                    'id': product.id,
                    'name': product.name,
                    'code': product.code,
                    'price': float(product.selling_price),
                    'unit': product.unit.name if product.unit else '',
                    'stock': 0
                })
        
        context['products'] = json.dumps(products_list)
        context['today'] = timezone.now().date()
        return context
    
    def form_valid(self, form):
        try:
            form.instance.created_by = self.request.user
            form.instance.status = 'draft'
            
            # Save the order first
            response = super().form_valid(form)
            
            # Generate order number if not exists
            if not self.object.order_number:
                from datetime import datetime
                import uuid
                now = datetime.now()
                
                # Try to generate unique order number
                max_attempts = 100
                for attempt in range(max_attempts):
                    order_count = Order.objects.filter(
                        created_at__date=now.date()
                    ).count() + attempt + 1
                    
                    potential_order_number = f"ORD{now.strftime('%Y%m%d')}{order_count:03d}"
                    
                    # Check if this order number already exists
                    if not Order.objects.filter(order_number=potential_order_number).exists():
                        self.object.order_number = potential_order_number
                        break
                else:
                    # Fallback: use UUID if we can't generate unique number
                    self.object.order_number = f"ORD{now.strftime('%Y%m%d')}{str(uuid.uuid4())[:6].upper()}"
                
                self.object.save()
            
            # Create order details from form data
            products_data = self.request.POST.getlist('products')
            total_amount = 0
            
            for product_json in products_data:
                if product_json:
                    try:
                        product_data = json.loads(product_json)
                        product = Product.objects.get(id=product_data['id'])
                        quantity = float(product_data['quantity'])
                        unit_price = float(product_data['price'])
                        line_total = quantity * unit_price
                        
                        OrderDetail.objects.create(
                            order=self.object,
                            product=product,
                            quantity=quantity,
                            unit_price=unit_price,
                            total_price=line_total
                        )
                        total_amount += line_total
                    except (json.JSONDecodeError, ValueError, Product.DoesNotExist) as e:
                        print(f"Error processing product data: {e}")
                        continue
            
            # Calculate totals
            discount_percent = float(self.request.POST.get('discount', 0))
            discount_amount = total_amount * (discount_percent / 100)
            final_total = total_amount - discount_amount
            
            # Update order totals
            self.object.subtotal = total_amount
            self.object.discount_amount = discount_amount
            self.object.total_amount = final_total
            self.object.save()
            
            messages.success(self.request, f'Tạo đơn hàng #{self.object.order_number} thành công!')
            return response
            
        except Exception as e:
            messages.error(self.request, f'Lỗi tạo đơn hàng: {str(e)}')
            return self.form_invalid(form)

class OrderUpdateView(LoginRequiredMixin, UpdateView):
    model = Order
    template_name = 'orders/update.html'
    fields = ['farmer', 'customer', 'order_type', 'delivery_date', 'shipping_address', 'shipping_contact', 'shipping_phone', 'notes', 'status', 'payment_status']
    context_object_name = 'order'
    
    def get_success_url(self):
        return reverse_lazy('orders:detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['farmers'] = Farmer.objects.filter(is_active=True)
        context['customers'] = Customer.objects.filter(is_active=True)
        context['products'] = list(Product.objects.select_related('unit').values(
            'id', 'name', 'code', 'selling_price', 'unit__name'
        ).annotate(unit=models.F('unit__name'), price=models.F('selling_price')))
        context['order_details'] = OrderDetail.objects.filter(order=self.object).select_related('product')
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Cập nhật đơn hàng thành công!')
        return super().form_valid(form)

class OrderDeleteView(LoginRequiredMixin, DeleteView):
    model = Order
    template_name = 'orders/delete.html'
    context_object_name = 'order'
    success_url = reverse_lazy('orders:list')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        
        # Delete all related order details first
        OrderDetail.objects.filter(order=self.object).delete()
        
        self.object.delete()
        messages.success(request, f'Đã xóa đơn hàng #{self.object.order_number}!')
        return redirect(success_url)


# API Views for Postman/External Integration
@method_decorator(csrf_exempt, name='dispatch')
class OrderAPICreateView(View):
    """API endpoint để tạo đơn hàng qua JSON"""
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['partner_id', 'order_type', 'delivery_date', 'order_details']
            for field in required_fields:
                if field not in data:
                    return JsonResponse({
                        'success': False,
                        'error': f'Missing required field: {field}'
                    }, status=400)
            # Get farmer or customer based on order type
            farmer = None
            customer = None
            shipping_address = data.get('shipping_address', '')
            
            if data['order_type'] in ['purchase']:
                # Order from farmer
                try:
                    farmer = Farmer.objects.get(id=data['partner_id'])
                    shipping_address = shipping_address or farmer.address
                except Farmer.DoesNotExist:
                    return JsonResponse({
                        'success': False,
                        'error': f'Farmer with ID {data["partner_id"]} not found'
                    }, status=400)
            else:
                # Order to customer
                try:
                    customer = Customer.objects.get(id=data['partner_id'])
                    shipping_address = shipping_address or customer.address
                except Customer.DoesNotExist:
                    return JsonResponse({
                        'success': False,
                        'error': f'Customer with ID {data["partner_id"]} not found'
                    }, status=400)
            
            # Create order
            with transaction.atomic():
                order = Order.objects.create(
                    order_type=data['order_type'],
                    farmer=farmer,
                    customer=customer,
                    delivery_date=data['delivery_date'],
                    shipping_address=shipping_address,
                    payment_status=data.get('payment_status', 'pending'),
                    notes=data.get('notes', ''),
                    created_by_id=data.get('created_by_id', 1)  # Default user ID
                )
                
                # Create order details
                total_amount = 0
                for detail_data in data['order_details']:
                    try:
                        product = Product.objects.get(id=detail_data['product_id'])
                    except Product.DoesNotExist:
                        return JsonResponse({
                            'success': False,
                            'error': f'Product with ID {detail_data["product_id"]} not found'
                        }, status=400)
                    
                    quantity = detail_data['quantity']
                    unit_price = detail_data.get('unit_price', product.selling_price)
                    total_price = quantity * unit_price
                    
                    OrderDetail.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        unit_price=unit_price,
                        total_price=total_price
                    )
                    
                    total_amount += total_price
                
                # Update order totals
                order.subtotal = total_amount
                order.discount_amount = data.get('discount_amount', 0)
                order.total_amount = total_amount - order.discount_amount
                order.save()
                
                return JsonResponse({
                    'success': True,
                    'order_id': order.id,
                    'order_number': order.order_number,
                    'total_amount': float(order.total_amount),
                    'message': 'Order created successfully'
                })
                
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid JSON format'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class OrderAPIDetailView(View):
    """API endpoint để lấy thông tin đơn hàng"""
    
    def get(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
            order_details = OrderDetail.objects.filter(order=order)
            
            response_data = {
                'success': True,
                'order': {
                    'id': order.id,
                    'order_number': order.order_number,
                    'order_type': order.order_type,
                    'partner': {
                        'id': order.farmer.id if order.farmer else (order.customer.id if order.customer else None),
                        'name': order.farmer.farm_name if order.farmer else (order.customer.full_name if order.customer else 'N/A'),
                        'type': 'farmer' if order.farmer else 'customer',
                        'code': order.farmer.farmer_code if order.farmer else (order.customer.customer_code if order.customer else 'N/A')
                    },
                    'delivery_date': order.delivery_date.isoformat() if order.delivery_date else None,
                    'shipping_address': order.shipping_address,
                    'payment_status': order.payment_status,
                    'status': order.status,
                    'subtotal': float(order.subtotal),
                    'discount_amount': float(order.discount_amount),
                    'total_amount': float(order.total_amount),
                    'notes': order.notes,
                    'created_at': order.created_at.isoformat(),
                    'order_details': [
                        {
                            'id': detail.id,
                            'product': {
                                'id': detail.product.id,
                                'code': detail.product.code,
                                'name': detail.product.name
                            },
                            'quantity': float(detail.quantity),
                            'unit_price': float(detail.unit_price),
                            'total_price': float(detail.total_price)
                        }
                        for detail in order_details
                    ]
                }
            }
            
            return JsonResponse(response_data)
            
        except Order.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': f'Order with ID {pk} not found'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
