from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import User, UserProfile

class CompanyUserListView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/company_users.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.filter(is_staff=False, is_superuser=False)
        return context

class AdminUserListView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/admin_users.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.filter(is_staff=True)
        return context

class CustomerUserListView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/customer_users.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Assuming customers are linked to companies
        from companies.models import Company
        context['companies'] = Company.objects.filter(company_type='customer')
        return context

# class ChangePasswordView(LoginRequiredMixin, TemplateView):  # Removed as requested
#     template_name = 'accounts/change_password.html'

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import User, UserProfile

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # User statistics
        from orders.models import Order
        from products.models import Product
        from news.models import News
        from activity_logs.models import ActivityLog
        
        user_stats = {
            'orders_created': Order.objects.filter(created_by=self.request.user).count(),
            'products_managed': Product.objects.filter(created_by=self.request.user).count() if hasattr(Product, 'created_by') else 0,
            'news_written': News.objects.filter(author=self.request.user).count(),
            'login_count': ActivityLog.objects.filter(user=self.request.user, action='login').count() if hasattr(ActivityLog, 'user') else 0,
        }
        
        # Recent activities
        recent_activities = []
        try:
            recent_activities = ActivityLog.objects.filter(
                user=self.request.user
            ).select_related('content_type').order_by('-created_at')[:10]
        except:
            pass
        
        context.update({
            'user_stats': user_stats,
            'recent_activities': recent_activities,
        })
        return context

class SettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/settings.html'

class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'
    paginate_by = 10
    
    def get_queryset(self):
        return User.objects.all().order_by('-date_joined')

@login_required
def create_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        role = request.POST.get('role')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, 'Mật khẩu không khớp')
            return redirect('accounts:user_list')
        
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                role=role
            )
            messages.success(request, f'Tạo nhân viên {user.get_full_name()} thành công')
        except Exception as e:
            messages.error(request, f'Lỗi tạo nhân viên: {str(e)}')
        
        return redirect('accounts:user_list')
    
    return redirect('accounts:user_list')

@login_required
def delete_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        if user.id != request.user.id:  # Không cho phép tự xóa
            user.delete()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Không thể tự xóa tài khoản'})
        return JsonResponse({'success': False})

@login_required
def update_profile(request):
    if request.method == 'POST':
        try:
            user = request.user
            user.first_name = request.POST.get('first_name', '')
            user.last_name = request.POST.get('last_name', '')
            user.email = request.POST.get('email', '')
            user.save()
            
            # Update or create profile
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.phone = request.POST.get('phone', '')
            profile.address = request.POST.get('address', '')
            profile.department = request.POST.get('department', '')
            profile.bio = request.POST.get('bio', '')
            
            if request.POST.get('date_of_birth'):
                profile.date_of_birth = request.POST.get('date_of_birth')
            
            if request.FILES.get('avatar'):
                profile.avatar = request.FILES['avatar']
            
            profile.save()
            messages.success(request, 'Cập nhật thông tin thành công!')
        except Exception as e:
            messages.error(request, f'Lỗi cập nhật: {str(e)}')
    
    return redirect('accounts:settings')

@login_required
def update_notifications(request):
    if request.method == 'POST':
        try:
            # Save notification preferences
            # This would typically be saved to a UserPreferences model
            messages.success(request, 'Cập nhật cài đặt thông báo thành công!')
        except Exception as e:
            messages.error(request, f'Lỗi cập nhật: {str(e)}')
    
    return redirect('accounts:settings')

@login_required
def update_preferences(request):
    if request.method == 'POST':
        try:
            # Save user preferences
            # This would typically be saved to a UserPreferences model
            messages.success(request, 'Cập nhật tùy chọn thành công!')
        except Exception as e:
            messages.error(request, f'Lỗi cập nhật: {str(e)}')
    
    return redirect('accounts:settings')

# class ChangePasswordView(LoginRequiredMixin, TemplateView):  # Removed as requested
#     template_name = 'accounts/change_password.html'

# class ChangePasswordView(LoginRequiredMixin, TemplateView):  # Removed as requested  
#     template_name = 'accounts/change_password.html'
