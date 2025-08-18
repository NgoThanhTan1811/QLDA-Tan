from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db import models
from .models import Product, Category, Unit

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 10
    
    def get_queryset(self):
        return Product.objects.select_related('category', 'unit').all()

class ProductCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'products/product_create.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        context['units'] = Unit.objects.all()
        return context
    
    def post(self, request):
        try:
            product = Product.objects.create(
                code=request.POST.get('code'),
                name=request.POST.get('name'),
                category_id=request.POST.get('category'),
                unit_id=request.POST.get('unit'),
                description=request.POST.get('description', ''),
                origin=request.POST.get('origin'),
                quality_grade=request.POST.get('quality_grade'),
                cost_price=request.POST.get('cost_price') or 0,
                selling_price=request.POST.get('selling_price') or 0,
                export_price=request.POST.get('export_price') or 0,
                shelf_life_days=request.POST.get('shelf_life_days') or None,
                storage_temperature_min=request.POST.get('storage_temperature_min') or None,
                storage_temperature_max=request.POST.get('storage_temperature_max') or None,
                humidity_requirement=request.POST.get('humidity_requirement') or None,
                hs_code=request.POST.get('hs_code', ''),
                is_active=request.POST.get('is_active') == '1'
            )
            messages.success(request, f'Tạo sản phẩm {product.name} thành công!')
            return redirect('products:list')
        except Exception as e:
            messages.error(request, f'Lỗi tạo sản phẩm: {str(e)}')
            return self.get(request)

class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get stock information
        try:
            from inventory.models import InventoryStock
            context['stock_info'] = InventoryStock.objects.filter(
                product=self.object
            ).select_related('warehouse')
        except:
            context['stock_info'] = None
        return context

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'products/delete.html'
    success_url = reverse_lazy('products:list')
    
    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        messages.success(request, f'Đã xóa sản phẩm "{product.name}" thành công!')
        return super().delete(request, *args, **kwargs)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'products/update.html'
    fields = ['code', 'name', 'category', 'unit', 'description', 'origin', 'quality_grade', 
              'cost_price', 'selling_price', 'export_price', 'shelf_life_days',
              'storage_temperature_min', 'storage_temperature_max', 'humidity_requirement',
              'hs_code', 'is_active']
    
    def get_success_url(self):
        return reverse_lazy('products:detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        context['units'] = Unit.objects.all()
        return context
    
    def form_valid(self, form):
        messages.success(self.request, f'Cập nhật sản phẩm {form.instance.name} thành công!')
        return super().form_valid(form)

class CategoryListView(LoginRequiredMixin, TemplateView):
    template_name = 'products/category_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.annotate(
            product_count=models.Count('products')  # Fix: 'product' -> 'products'
        ).all()
        return context
    
    def post(self, request):
        try:
            Category.objects.create(
                name=request.POST.get('name'),
                description=request.POST.get('description', ''),
                is_active=request.POST.get('is_active') == '1'
            )
            messages.success(request, 'Tạo danh mục thành công!')
        except Exception as e:
            messages.error(request, f'Lỗi tạo danh mục: {str(e)}')
        return redirect('products:categories')
