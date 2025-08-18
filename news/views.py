from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.urls import reverse_lazy
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.db.models import Q
from django.utils.text import slugify
import json
from .models import News, NewsCategory

class NewsListView(LoginRequiredMixin, ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news'
    paginate_by = 10
    
    def get_queryset(self):
        return News.objects.select_related('author', 'category').all().order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news = self.get_queryset()
        
        context.update({
            'published_count': news.filter(status='published').count(),
            'draft_count': news.filter(status='draft').count(),
            'categories': NewsCategory.objects.all(),
        })
        return context

class NewsDetailView(LoginRequiredMixin, DetailView):
    model = News
    template_name = 'news/detail.html'
    context_object_name = 'news'

class NewsCreateView(LoginRequiredMixin, CreateView):
    model = News
    template_name = 'news/create.html'
    fields = ['title', 'summary', 'content', 'category', 'news_type', 'status', 'priority']
    success_url = reverse_lazy('news:list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = NewsCategory.objects.all()
        return context
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        if form.instance.status == 'published':
            form.instance.publish_date = timezone.now()
        messages.success(self.request, 'Tạo tin tức thành công!')
        return super().form_valid(form)

class NewsUpdateView(LoginRequiredMixin, UpdateView):
    model = News
    template_name = 'news/update.html'
    fields = ['title', 'summary', 'content', 'category', 'news_type', 'status', 'priority']
    
    def get_success_url(self):
        return reverse_lazy('news:detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = NewsCategory.objects.all()
        return context
    
    def form_valid(self, form):
        if form.instance.status == 'published' and not form.instance.publish_date:
            form.instance.publish_date = timezone.now()
        messages.success(self.request, 'Cập nhật tin tức thành công!')
        return super().form_valid(form)

class NewsDeleteView(LoginRequiredMixin, DeleteView):
    model = News
    template_name = 'news/delete.html'
    context_object_name = 'news'
    success_url = reverse_lazy('news:list')
    
    def delete(self, request, *args, **kwargs):
        news = self.get_object()
        messages.success(request, f'Đã xóa tin tức "{news.title}" thành công!')
        return super().delete(request, *args, **kwargs)

# News API Views
@method_decorator(csrf_exempt, name='dispatch')
class NewsAPICreateView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['title', 'summary', 'content', 'category_id', 'news_type']
            for field in required_fields:
                if not data.get(field):
                    return JsonResponse({
                        'success': False,
                        'error': f'Trường {field} là bắt buộc'
                    }, status=400)
            
            # Check if category exists
            try:
                category = NewsCategory.objects.get(id=data['category_id'])
            except NewsCategory.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': 'Danh mục tin tức không tồn tại'
                }, status=400)
            
            # Validate choices
            valid_news_types = [choice[0] for choice in News.NEWS_TYPE_CHOICES]
            if data['news_type'] not in valid_news_types:
                return JsonResponse({
                    'success': False,
                    'error': f'Loại tin không hợp lệ. Chọn từ: {", ".join(valid_news_types)}'
                }, status=400)
            
            valid_statuses = [choice[0] for choice in News.STATUS_CHOICES]
            status = data.get('status', 'draft')
            if status not in valid_statuses:
                return JsonResponse({
                    'success': False,
                    'error': f'Trạng thái không hợp lệ. Chọn từ: {", ".join(valid_statuses)}'
                }, status=400)
            
            valid_priorities = [choice[0] for choice in News.PRIORITY_CHOICES]
            priority = data.get('priority', 'normal')
            if priority not in valid_priorities:
                return JsonResponse({
                    'success': False,
                    'error': f'Độ ưu tiên không hợp lệ. Chọn từ: {", ".join(valid_priorities)}'
                }, status=400)
            
            with transaction.atomic():
                # Generate unique slug
                base_slug = slugify(data['title'])
                slug = base_slug
                counter = 1
                while News.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                
                news = News.objects.create(
                    title=data['title'],
                    slug=slug,
                    summary=data['summary'],
                    content=data['content'],
                    category=category,
                    news_type=data['news_type'],
                    status=status,
                    priority=priority,
                    author_id=1,  # You might want to get this from request.user
                    publish_date=timezone.now() if status == 'published' else None,
                    expire_date=data.get('expiry_date'),
                    is_featured=data.get('is_featured', False)
                )
            
            return JsonResponse({
                'success': True,
                'message': 'Tạo tin tức thành công',
                'data': {
                    'id': news.id,
                    'title': news.title,
                    'slug': news.slug,
                    'summary': news.summary,
                    'content': news.content,
                    'category_id': news.category.id,
                    'category_name': news.category.name,
                    'news_type': news.news_type,
                    'status': news.status,
                    'priority': news.priority,
                    'author_id': news.author.id,
                    'author_name': news.author.get_full_name(),
                    'publish_date': news.publish_date.isoformat() if news.publish_date else None,
                    'expire_date': news.expire_date.isoformat() if news.expire_date else None,
                    'is_featured': news.is_featured,
                    'view_count': news.view_count,
                    'created_at': news.created_at.isoformat(),
                    'updated_at': news.updated_at.isoformat()
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

class NewsAPIDetailView(View):
    def get(self, request, pk):
        try:
            news = News.objects.select_related('author', 'category').get(pk=pk)
            
            # Increment view count
            news.view_count += 1
            news.save()
            
            return JsonResponse({
                'success': True,
                'data': {
                    'id': news.id,
                    'title': news.title,
                    'slug': news.slug,
                    'summary': news.summary,
                    'content': news.content,
                    'category': {
                        'id': news.category.id,
                        'name': news.category.name,
                        'color': news.category.color
                    },
                    'news_type': news.news_type,
                    'news_type_display': news.get_news_type_display(),
                    'status': news.status,
                    'status_display': news.get_status_display(),
                    'priority': news.priority,
                    'priority_display': news.get_priority_display(),
                    'author': {
                        'id': news.author.id,
                        'name': news.author.get_full_name(),
                        'email': news.author.email
                    },
                    'publish_date': news.publish_date.isoformat() if news.publish_date else None,
                    'expire_date': news.expire_date.isoformat() if news.expire_date else None,
                    'is_featured': news.is_featured,
                    'view_count': news.view_count,
                    'created_at': news.created_at.isoformat(),
                    'updated_at': news.updated_at.isoformat()
                }
            })
        except News.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Tin tức không tồn tại'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Lỗi server: {str(e)}'
            }, status=500)

class NewsAPIListView(View):
    def get(self, request):
        try:
            news_queryset = News.objects.select_related('author', 'category').filter(is_active=True)
            
            # Filter by status
            status = request.GET.get('status')
            if status:
                news_queryset = news_queryset.filter(status=status)
            
            # Filter by category
            category_id = request.GET.get('category_id')
            if category_id:
                news_queryset = news_queryset.filter(category_id=category_id)
            
            # Filter by news type
            news_type = request.GET.get('news_type')
            if news_type:
                news_queryset = news_queryset.filter(news_type=news_type)
            
            # Search functionality
            search = request.GET.get('search')
            if search:
                news_queryset = news_queryset.filter(
                    Q(title__icontains=search) |
                    Q(summary__icontains=search) |
                    Q(content__icontains=search)
                )
            
            # Filter by featured
            is_featured = request.GET.get('is_featured')
            if is_featured == 'true':
                news_queryset = news_queryset.filter(is_featured=True)
            
            # Order by
            order_by = request.GET.get('order_by', '-created_at')
            if order_by in ['created_at', '-created_at', 'title', '-title', 'views_count', '-views_count']:
                news_queryset = news_queryset.order_by(order_by)
            
            data = []
            for news in news_queryset:
                data.append({
                    'id': news.id,
                    'title': news.title,
                    'slug': news.slug,
                    'summary': news.summary,
                    'category': {
                        'id': news.category.id,
                        'name': news.category.name,
                        'color': news.category.color
                    },
                    'news_type': news.news_type,
                    'news_type_display': news.get_news_type_display(),
                    'status': news.status,
                    'status_display': news.get_status_display(),
                    'priority': news.priority,
                    'priority_display': news.get_priority_display(),
                    'author_name': news.author.get_full_name(),
                    'publish_date': news.publish_date.isoformat() if news.publish_date else None,
                    'is_featured': news.is_featured,
                    'views_count': news.views_count,
                    'created_at': news.created_at.isoformat()
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

class NewsCategoryAPIListView(View):
    def get(self, request):
        try:
            categories = NewsCategory.objects.all().order_by('name')
            
            data = []
            for category in categories:
                data.append({
                    'id': category.id,
                    'name': category.name,
                    'description': category.description,
                    'color': category.color,
                    'is_active': category.is_active,
                    'news_count': category.news.count()
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
