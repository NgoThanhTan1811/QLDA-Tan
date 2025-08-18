from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.db.models import Sum, Count, Q
from decimal import Decimal
from .models import Payment
from orders.models import Order

class PaymentListView(LoginRequiredMixin, TemplateView):
    template_name = 'payments/payment_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        payments = Payment.objects.select_related('order', 'order__company').all()
        
        # Filter by status if provided
        status_filter = self.request.GET.get('status')
        if status_filter:
            if status_filter == 'overdue':
                payments = payments.filter(
                    status='pending', 
                    due_date__lt=timezone.now().date()
                )
            else:
                payments = payments.filter(status=status_filter)
        
        context.update({
            'payments': payments,
            'status_filter': status_filter,
            'total_payments': payments.aggregate(total=Sum('amount'))['total'] or Decimal('0'),
            'pending_count': Payment.objects.filter(status='pending').count(),
            'completed_count': Payment.objects.filter(status='completed').count(),
            'overdue_count': Payment.objects.filter(
                status='pending', 
                due_date__lt=timezone.now().date()
            ).count(),
            'orders': Order.objects.filter(payment_status__in=['pending', 'partial']),
            'today': timezone.now().date(),
        })
        return context
    
    def post(self, request):
        try:
            order_id = request.POST.get('order')
            order = None
            company = None
            
            if order_id:
                order = Order.objects.get(id=order_id)
                company = order.company
            
            Payment.objects.create(
                order=order,
                company=company,
                payment_type=request.POST.get('payment_type', 'inbound'),
                amount=Decimal(request.POST.get('amount', '0')),
                payment_method=request.POST.get('payment_method'),
                currency=request.POST.get('currency', 'VND'),
                due_date=request.POST.get('due_date') or timezone.now().date(),
                payment_date=request.POST.get('payment_date') or timezone.now().date(),
                notes=request.POST.get('notes', ''),
                status='pending',
                created_by=request.user
            )
            messages.success(request, 'Tạo thanh toán thành công!')
        except Exception as e:
            messages.error(request, f'Lỗi tạo thanh toán: {str(e)}')
        return redirect('payments:list')

class PaymentCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'payments/create.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(
            payment_status__in=['pending', 'partial']
        ).select_related('company')
        context['today'] = timezone.now().date()
        return context
    
    def post(self, request):
        try:
            order_id = request.POST.get('order')
            order = None
            company = None
            
            if order_id:
                order = Order.objects.get(id=order_id)
                company = order.company
            
            payment = Payment.objects.create(
                order=order,
                company=company,
                payment_type=request.POST.get('payment_type', 'inbound'),
                amount=Decimal(request.POST.get('amount', '0')),
                payment_method=request.POST.get('payment_method'),
                currency=request.POST.get('currency', 'VND'),
                due_date=request.POST.get('due_date') or timezone.now().date(),
                payment_date=request.POST.get('payment_date') or timezone.now().date(),
                notes=request.POST.get('notes', ''),
                status='pending',
                created_by=request.user
            )
            messages.success(request, f'Tạo thanh toán {payment.payment_code or "Auto"} thành công!')
            return redirect('payments:detail', pk=payment.id)
        except Exception as e:
            messages.error(request, f'Lỗi tạo thanh toán: {str(e)}')
            return redirect('payments:create')

class PaymentDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'payments/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        payment_id = self.kwargs.get('pk')
        try:
            payment = Payment.objects.select_related('order', 'company', 'created_by').get(id=payment_id)
            context['payment'] = payment
        except Payment.DoesNotExist:
            context['payment'] = None
        context['today'] = timezone.now().date()
        return context

class PaymentConfirmView(LoginRequiredMixin, View):
    def post(self, request, pk):
        try:
            payment = get_object_or_404(Payment, id=pk)
            if payment.status == 'pending':
                payment.status = 'completed'
                payment.payment_date = timezone.now().date()
                payment.save()
                
                # Update order payment status if needed
                if payment.order:
                    order = payment.order
                    total_payments = Payment.objects.filter(
                        order=order, 
                        status='completed'
                    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
                    
                    if total_payments >= order.total_amount:
                        order.payment_status = 'completed'
                    else:
                        order.payment_status = 'partial'
                    order.save()
                
                messages.success(request, f'Xác nhận thanh toán {payment.payment_code} thành công!')
            else:
                messages.warning(request, 'Thanh toán này đã được xác nhận trước đó.')
        except Exception as e:
            messages.error(request, f'Lỗi xác nhận thanh toán: {str(e)}')
        
        return redirect('payments:list')

class PaymentPrintView(LoginRequiredMixin, TemplateView):
    template_name = 'payments/print_invoice.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        payment_id = self.kwargs.get('pk')
        try:
            payment = Payment.objects.select_related('order', 'company', 'created_by').get(id=payment_id)
            context['payment'] = payment
        except Payment.DoesNotExist:
            context['payment'] = None
        context['today'] = timezone.now()
        return context
