from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count, Sum, F, Q
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import json
from .models import InventoryStock, Warehouse, StockMovement, StockTaking
from products.models import Product

User = get_user_model()

class StockListView(LoginRequiredMixin, ListView):
    model = InventoryStock
    template_name = 'inventory/stock_list.html'
    context_object_name = 'stocks'
    paginate_by = 10
    
    def get_queryset(self):
        return InventoryStock.objects.select_related(
            'product', 'warehouse', 'product__unit'
        ).annotate(
            total_value=F('quantity') * F('product__cost_price')
        ).order_by('product__name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stocks = self.get_queryset()
        
        context.update({
            'total_products': stocks.values('product').distinct().count(),
            'total_stock': stocks.aggregate(total=Sum('quantity'))['total'] or 0,
            'low_stock_count': stocks.filter(quantity__lte=F('min_stock_level')).count(),
            'warehouse_count': Warehouse.objects.count(),
        })
        return context

class StockDetailView(LoginRequiredMixin, DetailView):
    model = InventoryStock
    template_name = 'inventory/stock_detail.html'
    context_object_name = 'stock'

class StockCreateView(LoginRequiredMixin, CreateView):
    model = InventoryStock
    template_name = 'inventory/stock_create.html'
    fields = ['product', 'warehouse', 'quantity', 'min_stock_level', 'max_stock_level']
    success_url = reverse_lazy('inventory:stock')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(is_active=True)
        context['warehouses'] = Warehouse.objects.filter(is_active=True)
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Tạo stock thành công!')
        return super().form_valid(form)

class StockUpdateView(LoginRequiredMixin, UpdateView):
    model = InventoryStock
    template_name = 'inventory/stock_update.html'
    fields = ['product', 'warehouse', 'quantity', 'min_stock_level', 'max_stock_level']
    
    def get_success_url(self):
        return reverse_lazy('inventory:stock')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(is_active=True)
        context['warehouses'] = Warehouse.objects.filter(is_active=True)
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Cập nhật stock thành công!')
        return super().form_valid(form)

class StockDeleteView(LoginRequiredMixin, DeleteView):
    model = InventoryStock
    template_name = 'inventory/stock_delete.html'
    success_url = reverse_lazy('inventory:stock')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Xóa stock thành công!')
        return super().delete(request, *args, **kwargs)

class WarehouseListView(LoginRequiredMixin, ListView):
    model = Warehouse
    template_name = 'inventory/warehouse_list.html'
    context_object_name = 'warehouses'
    paginate_by = 10
    
    def get_queryset(self):
        return Warehouse.objects.select_related('manager').annotate(
            stock_count=Count('inventorystock'),
            used_capacity=Sum('inventorystock__quantity', default=0)
        ).all()

class WarehouseDetailView(LoginRequiredMixin, DetailView):
    model = Warehouse
    template_name = 'inventory/warehouse_detail.html'
    context_object_name = 'warehouse'

class WarehouseCreateView(LoginRequiredMixin, CreateView):
    model = Warehouse
    template_name = 'inventory/warehouse_create.html'
    fields = ['name', 'code', 'address', 'capacity', 'manager', 'is_active']
    success_url = reverse_lazy('inventory:warehouses')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['managers'] = User.objects.filter(is_staff=True)
        return context
    
    def form_valid(self, form):
        try:
            messages.success(self.request, f'Tạo kho hàng "{form.instance.name}" thành công!')
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f'Lỗi tạo kho hàng: {str(e)}')
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Có lỗi trong quá trình tạo kho hàng. Vui lòng kiểm tra lại.')
        return super().form_invalid(form)

class WarehouseUpdateView(LoginRequiredMixin, UpdateView):
    model = Warehouse
    template_name = 'inventory/warehouse_update.html'
    fields = ['name', 'code', 'address', 'capacity', 'manager', 'is_active']
    
    def get_success_url(self):
        return reverse_lazy('inventory:warehouse_detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['managers'] = User.objects.filter(is_staff=True)
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Cập nhật kho hàng thành công!')
        return super().form_valid(form)

class WarehouseDeleteView(LoginRequiredMixin, DeleteView):
    model = Warehouse
    template_name = 'inventory/warehouse_delete.html'
    success_url = reverse_lazy('inventory:warehouses')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Xóa kho hàng thành công!')
        return super().delete(request, *args, **kwargs)

class MovementListView(LoginRequiredMixin, ListView):
    model = StockMovement
    template_name = 'inventory/movement_list.html'
    context_object_name = 'movements'
    paginate_by = 10
    
    def get_queryset(self):
        return StockMovement.objects.select_related(
            'warehouse', 'product', 'created_by'
        ).all().order_by('-created_at')

class MovementCreateView(LoginRequiredMixin, CreateView):
    model = StockMovement
    template_name = 'inventory/movement_create.html'
    fields = ['warehouse', 'product', 'movement_type', 'quantity', 'unit_cost', 'notes']
    success_url = reverse_lazy('inventory:movements')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['warehouses'] = Warehouse.objects.filter(is_active=True)
        context['products'] = Product.objects.filter(is_active=True)
        return context
    
    def form_valid(self, form):
        try:
            form.instance.created_by = self.request.user
            response = super().form_valid(form)
            
            # Signal sẽ tự động update stock
            messages.success(self.request, f'Tạo phiếu {form.instance.get_movement_type_display()} thành công!')
            return response
            
        except Exception as e:
            messages.error(self.request, f'Lỗi tạo phiếu xuất nhập kho: {str(e)}')
            return self.form_invalid(form)

class StockTakingListView(LoginRequiredMixin, ListView):
    model = StockTaking
    template_name = 'inventory/stock_taking.html'
    context_object_name = 'stock_takings'
    paginate_by = 10
    
    def get_queryset(self):
        return StockTaking.objects.select_related(
            'warehouse', 'created_by'
        ).all().order_by('-created_at')

# Warehouse API Views
@method_decorator(csrf_exempt, name='dispatch')
class WarehouseAPICreateView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['name', 'code', 'address', 'capacity']
            for field in required_fields:
                if not data.get(field):
                    return JsonResponse({
                        'success': False,
                        'error': f'Trường {field} là bắt buộc'
                    }, status=400)
            
            # Check for duplicate code
            if Warehouse.objects.filter(code=data['code']).exists():
                return JsonResponse({
                    'success': False,
                    'error': 'Mã kho đã tồn tại'
                }, status=400)
            
            # Check for duplicate name
            if Warehouse.objects.filter(name=data['name']).exists():
                return JsonResponse({
                    'success': False,
                    'error': 'Tên kho đã tồn tại'
                }, status=400)
            
            with transaction.atomic():
                # Get manager if provided
                manager = None
                if data.get('manager_id'):
                    try:
                        manager = User.objects.get(id=data['manager_id'])
                    except User.DoesNotExist:
                        return JsonResponse({
                            'success': False,
                            'error': 'Quản lý kho không tồn tại'
                        }, status=400)
                
                warehouse = Warehouse.objects.create(
                    name=data['name'],
                    code=data['code'],
                    address=data['address'],
                    manager=manager,
                    capacity=float(data['capacity']),
                    is_active=data.get('is_active', True)
                )
            
            return JsonResponse({
                'success': True,
                'message': 'Tạo kho thành công',
                'data': {
                    'id': warehouse.id,
                    'name': warehouse.name,
                    'code': warehouse.code,
                    'address': warehouse.address,
                    'manager_id': warehouse.manager.id if warehouse.manager else None,
                    'manager_name': warehouse.manager.get_full_name() if warehouse.manager else None,
                    'capacity': float(warehouse.capacity),
                    'is_active': warehouse.is_active,
                    'created_at': warehouse.created_at.isoformat()
                }
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Dữ liệu JSON không hợp lệ'
            }, status=400)
        except ValueError as e:
            return JsonResponse({
                'success': False,
                'error': f'Dữ liệu không hợp lệ: {str(e)}'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Lỗi server: {str(e)}'
            }, status=500)

class WarehouseAPIDetailView(View):
    def get(self, request, pk):
        try:
            warehouse = Warehouse.objects.select_related('manager').get(pk=pk)
            
            # Get stock summary for this warehouse
            stock_summary = InventoryStock.objects.filter(warehouse=warehouse).aggregate(
                total_products=Count('product'),
                total_quantity=Sum('quantity'),
                low_stock_items=Count('id', filter=Q(quantity__lte=F('min_stock_level')))
            )
            
            return JsonResponse({
                'success': True,
                'data': {
                    'id': warehouse.id,
                    'name': warehouse.name,
                    'code': warehouse.code,
                    'address': warehouse.address,
                    'manager_id': warehouse.manager.id if warehouse.manager else None,
                    'manager_name': warehouse.manager.get_full_name() if warehouse.manager else None,
                    'manager_email': warehouse.manager.email if warehouse.manager else None,
                    'capacity': float(warehouse.capacity),
                    'is_active': warehouse.is_active,
                    'created_at': warehouse.created_at.isoformat(),
                    'stock_summary': {
                        'total_products': stock_summary['total_products'] or 0,
                        'total_quantity': float(stock_summary['total_quantity'] or 0),
                        'low_stock_items': stock_summary['low_stock_items'] or 0
                    }
                }
            })
        except Warehouse.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Kho không tồn tại'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Lỗi server: {str(e)}'
            }, status=500)

class WarehouseAPIListView(View):
    def get(self, request):
        try:
            warehouses = Warehouse.objects.select_related('manager').filter(is_active=True).order_by('name')
            
            # Search functionality
            search = request.GET.get('search')
            if search:
                warehouses = warehouses.filter(
                    Q(name__icontains=search) |
                    Q(code__icontains=search) |
                    Q(address__icontains=search)
                )
            
            data = []
            for warehouse in warehouses:
                # Get basic stock stats
                stock_stats = InventoryStock.objects.filter(warehouse=warehouse).aggregate(
                    total_products=Count('product'),
                    total_quantity=Sum('quantity')
                )
                
                data.append({
                    'id': warehouse.id,
                    'name': warehouse.name,
                    'code': warehouse.code,
                    'address': warehouse.address,
                    'manager_name': warehouse.manager.get_full_name() if warehouse.manager else None,
                    'capacity': float(warehouse.capacity),
                    'is_active': warehouse.is_active,
                    'stock_summary': {
                        'total_products': stock_stats['total_products'] or 0,
                        'total_quantity': float(stock_stats['total_quantity'] or 0)
                    }
                })
            
            return JsonResponse({
                'success': True,
                'count': len(data),
                'data': data
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Lỗi server: {str(e)}'
            }, status=500)

# Stock Movement API Views
@method_decorator(csrf_exempt, name='dispatch')
class StockMovementAPICreateView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['movement_type', 'warehouse_id', 'items']
            for field in required_fields:
                if not data.get(field):
                    return JsonResponse({
                        'success': False,
                        'error': f'Trường {field} là bắt buộc'
                    }, status=400)
            
            # Validate movement_type
            valid_types = ['inbound', 'outbound', 'transfer', 'adjustment', 'damaged', 'expired']
            if data['movement_type'] not in valid_types:
                return JsonResponse({
                    'success': False,
                    'error': f'Loại phiếu không hợp lệ. Chọn từ: {", ".join(valid_types)}'
                }, status=400)
            
            # Check warehouse exists
            try:
                warehouse = Warehouse.objects.get(id=data['warehouse_id'])
            except Warehouse.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': 'Kho không tồn tại'
                }, status=400)
            
            with transaction.atomic():
                # Create movements for each item
                movements = []
                total_value = 0
                items_data = []
                
                for item_data in data['items']:
                    try:
                        product = Product.objects.get(id=item_data['product_id'])
                        quantity = float(item_data['quantity'])
                        unit_cost = float(item_data.get('unit_cost', 0))
                        total_cost = quantity * unit_cost
                        
                        # Create stock movement
                        movement = StockMovement.objects.create(
                            warehouse=warehouse,
                            product=product,
                            movement_type=data['movement_type'],
                            quantity=quantity,
                            unit_cost=unit_cost,
                            reference_type=data.get('reference_type', 'manual'),
                            reference_id=data.get('reference_id'),
                            notes=item_data.get('notes', ''),
                            created_by_id=1  # Replace with request.user.id when auth is implemented
                        )
                        
                        movements.append(movement)
                        total_value += total_cost
                        
                        # Update stock levels
                        stock, created = InventoryStock.objects.get_or_create(
                            warehouse=warehouse,
                            product=product,
                            defaults={'quantity': 0}
                        )
                        
                        if data['movement_type'] == 'inbound':
                            stock.quantity += quantity
                        elif data['movement_type'] == 'outbound':
                            if stock.quantity < quantity:
                                return JsonResponse({
                                    'success': False,
                                    'error': f'Không đủ tồn kho cho sản phẩm {product.name}. Tồn: {stock.quantity}, Xuất: {quantity}'
                                }, status=400)
                            stock.quantity -= quantity
                        elif data['movement_type'] == 'adjustment':
                            stock.quantity = quantity
                        
                        stock.save()
                        
                        items_data.append({
                            'id': movement.id,
                            'product': {
                                'id': product.id,
                                'name': product.name,
                                'code': product.code
                            },
                            'quantity': quantity,
                            'unit_cost': unit_cost,
                            'total_cost': total_cost,
                            'notes': movement.notes,
                            'created_at': movement.created_at.isoformat()
                        })
                        
                    except Product.DoesNotExist:
                        return JsonResponse({
                            'success': False,
                            'error': f'Sản phẩm ID {item_data["product_id"]} không tồn tại'
                        }, status=400)
                    except ValueError as e:
                        return JsonResponse({
                            'success': False,
                            'error': f'Dữ liệu số không hợp lệ: {str(e)}'
                        }, status=400)
                
                return JsonResponse({
                    'success': True,
                    'message': 'Tạo phiếu xuất nhập kho thành công',
                    'data': {
                        'warehouse': {
                            'id': warehouse.id,
                            'name': warehouse.name,
                            'code': warehouse.code
                        },
                        'movement_type': data['movement_type'],
                        'movement_type_display': dict(StockMovement.MOVEMENT_TYPE_CHOICES)[data['movement_type']],
                        'reference_type': data.get('reference_type', 'manual'),
                        'reference_id': data.get('reference_id'),
                        'total_items': len(items_data),
                        'total_value': total_value,
                        'created_at': movements[0].created_at.isoformat() if movements else None,
                        'items': items_data
                    }
                })
                
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Dữ liệu JSON không hợp lệ'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Lỗi server: {str(e)}'
            }, status=500)

# Stock Movement Detail API View
@method_decorator(csrf_exempt, name='dispatch')
class StockMovementAPIDetailView(View):
    def get(self, request, movement_id):
        try:
            movement = StockMovement.objects.select_related(
                'warehouse', 'product', 'created_by'
            ).get(id=movement_id)
            
            return JsonResponse({
                'success': True,
                'data': {
                    'id': movement.id,
                    'movement_type': movement.movement_type,
                    'movement_type_display': movement.get_movement_type_display(),
                    'warehouse': {
                        'id': movement.warehouse.id,
                        'name': movement.warehouse.name,
                        'code': movement.warehouse.code
                    },
                    'product': {
                        'id': movement.product.id,
                        'name': movement.product.name,
                        'code': movement.product.code
                    },
                    'quantity': float(movement.quantity),
                    'unit_cost': float(movement.unit_cost) if movement.unit_cost else None,
                    'reference_type': movement.reference_type,
                    'reference_id': movement.reference_id,
                    'notes': movement.notes,
                    'created_by': movement.created_by.username if movement.created_by else None,
                    'created_at': movement.created_at.isoformat(),
                    'updated_at': movement.updated_at.isoformat()
                }
            })
            
        except StockMovement.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Phiếu xuất nhập kho không tồn tại'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Lỗi server: {str(e)}'
            }, status=500)

# Stock Movement List API View
@method_decorator(csrf_exempt, name='dispatch')
class StockMovementAPIListView(View):
    def get(self, request):
        try:
            # Get query parameters
            movement_type = request.GET.get('movement_type')
            warehouse_id = request.GET.get('warehouse_id')
            product_id = request.GET.get('product_id')
            page = int(request.GET.get('page', 1))
            per_page = min(int(request.GET.get('per_page', 10)), 100)
            
            # Build queryset
            queryset = StockMovement.objects.select_related(
                'warehouse', 'product', 'created_by'
            )
            
            if movement_type:
                queryset = queryset.filter(movement_type=movement_type)
            if warehouse_id:
                queryset = queryset.filter(warehouse_id=warehouse_id)
            if product_id:
                queryset = queryset.filter(product_id=product_id)
            
            queryset = queryset.order_by('-created_at')
            
            # Pagination
            from django.core.paginator import Paginator
            paginator = Paginator(queryset, per_page)
            movements = paginator.get_page(page)
            
            data = []
            for movement in movements:
                data.append({
                    'id': movement.id,
                    'movement_type': movement.movement_type,
                    'movement_type_display': movement.get_movement_type_display(),
                    'warehouse': {
                        'id': movement.warehouse.id,
                        'name': movement.warehouse.name,
                        'code': movement.warehouse.code
                    },
                    'product': {
                        'id': movement.product.id,
                        'name': movement.product.name,
                        'code': movement.product.code
                    },
                    'quantity': float(movement.quantity),
                    'unit_cost': float(movement.unit_cost) if movement.unit_cost else None,
                    'reference_type': movement.reference_type,
                    'reference_id': movement.reference_id,
                    'notes': movement.notes,
                    'created_by': movement.created_by.username if movement.created_by else None,
                    'created_at': movement.created_at.isoformat()
                })
            
            return JsonResponse({
                'success': True,
                'data': data,
                'pagination': {
                    'current_page': page,
                    'per_page': per_page,
                    'total_pages': paginator.num_pages,
                    'total_items': paginator.count,
                    'has_next': movements.has_next(),
                    'has_previous': movements.has_previous()
                }
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Lỗi server: {str(e)}'
            }, status=500)
