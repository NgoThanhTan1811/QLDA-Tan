from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction, models
import json
from .models import Company

class CompanyListView(LoginRequiredMixin, ListView):
    model = Company
    template_name = 'companies/list.html'
    context_object_name = 'companies'
    paginate_by = 10

class CompanyDetailView(LoginRequiredMixin, DetailView):
    model = Company
    template_name = 'companies/detail.html'

class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = Company
    template_name = 'companies/create.html'
    fields = ['name', 'company_type', 'tax_code', 'address', 'phone', 'email', 'website', 'contact_person', 'contact_phone', 'contact_email', 'bank_name', 'bank_account', 'is_active']
    success_url = reverse_lazy('companies:list')
    
    def form_valid(self, form):
        try:
            messages.success(self.request, f'Tạo công ty "{form.instance.name}" thành công!')
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f'Có lỗi trong quá trình tạo công ty: {str(e)}')
            return self.form_invalid(form)

class CompanyUpdateView(LoginRequiredMixin, UpdateView):
    model = Company
    template_name = 'companies/update.html'
    fields = ['name', 'company_type', 'tax_code', 'address', 'phone', 'email', 'website', 'contact_person', 'contact_phone', 'contact_email', 'bank_name', 'bank_account', 'is_active']
    
    def get_success_url(self):
        return reverse_lazy('companies:detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, f'Cập nhật công ty "{form.instance.name}" thành công!')
        return super().form_valid(form)

class CompanyDeleteView(LoginRequiredMixin, DeleteView):
    model = Company
    template_name = 'companies/delete.html'
    success_url = reverse_lazy('companies:list')
    
    def delete(self, request, *args, **kwargs):
        company = self.get_object()
        messages.success(request, f'Xóa công ty "{company.name}" thành công!')
        return super().delete(request, *args, **kwargs)

# API Views
@method_decorator(csrf_exempt, name='dispatch')
class CompanyAPICreateView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            # Validate required fields
            required_fields = ['name', 'company_type', 'tax_code', 'address']
            for field in required_fields:
                if not data.get(field):
                    return JsonResponse({
                        'success': False,
                        'error': f'Trường {field} là bắt buộc'
                    }, status=400)
            
            # Check for duplicate tax_code
            if Company.objects.filter(tax_code=data['tax_code']).exists():
                return JsonResponse({
                    'success': False,
                    'error': 'Mã số thuế đã tồn tại'
                }, status=400)
            
            with transaction.atomic():
                company = Company.objects.create(
                    name=data['name'],
                    company_type=data['company_type'],
                    tax_code=data['tax_code'],
                    address=data['address'],
                    phone=data.get('phone', ''),
                    email=data.get('email', ''),
                    website=data.get('website', ''),
                    bank_name=data.get('bank_name', ''),
                    bank_account=data.get('bank_account', ''),
                    contact_person=data.get('contact_person', ''),
                    contact_phone=data.get('contact_phone', ''),
                    contact_email=data.get('contact_email', ''),
                    import_license=data.get('import_license', ''),
                    export_license=data.get('export_license', ''),
                    is_active=data.get('is_active', True)
                )
            
            return JsonResponse({
                'success': True,
                'message': 'Tạo công ty thành công',
                'data': {
                    'id': company.id,
                    'name': company.name,
                    'company_type': company.company_type,
                    'tax_code': company.tax_code,
                    'address': company.address,
                    'phone': company.phone,
                    'email': company.email,
                    'website': company.website,
                    'contact_person': company.contact_person,
                    'contact_phone': company.contact_phone,
                    'contact_email': company.contact_email,
                    'bank_name': company.bank_name,
                    'bank_account': company.bank_account,
                    'import_license': company.import_license,
                    'export_license': company.export_license,
                    'is_active': company.is_active,
                    'created_at': company.created_at.isoformat(),
                    'updated_at': company.updated_at.isoformat()
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

class CompanyAPIDetailView(View):
    def get(self, request, pk):
        try:
            company = Company.objects.get(pk=pk)
            return JsonResponse({
                'success': True,
                'data': {
                    'id': company.id,
                    'name': company.name,
                    'company_type': company.company_type,
                    'company_type_display': company.get_company_type_display(),
                    'tax_code': company.tax_code,
                    'address': company.address,
                    'phone': company.phone,
                    'email': company.email,
                    'website': company.website,
                    'contact_person': company.contact_person,
                    'contact_phone': company.contact_phone,
                    'contact_email': company.contact_email,
                    'bank_name': company.bank_name,
                    'bank_account': company.bank_account,
                    'import_license': company.import_license,
                    'export_license': company.export_license,
                    'is_active': company.is_active,
                    'created_at': company.created_at.isoformat(),
                    'updated_at': company.updated_at.isoformat()
                }
            })
        except Company.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Công ty không tồn tại'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Lỗi server: {str(e)}'
            }, status=500)

class CompanyAPIListView(View):
    def get(self, request):
        try:
            companies = Company.objects.filter(is_active=True).order_by('name')
            
            # Filter by company type if provided
            company_type = request.GET.get('type')
            if company_type:
                companies = companies.filter(company_type=company_type)
            
            # Search functionality
            search = request.GET.get('search')
            if search:
                companies = companies.filter(
                    models.Q(name__icontains=search) |
                    models.Q(tax_code__icontains=search) |
                    models.Q(contact_person__icontains=search)
                )
            
            data = []
            for company in companies:
                data.append({
                    'id': company.id,
                    'name': company.name,
                    'company_type': company.company_type,
                    'company_type_display': company.get_company_type_display(),
                    'tax_code': company.tax_code,
                    'address': company.address,
                    'phone': company.phone,
                    'email': company.email,
                    'contact_person': company.contact_person,
                    'contact_phone': company.contact_phone,
                    'is_active': company.is_active
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
        messages.success(request, f'Đã xóa công ty "{company.name}"!')
        return super().delete(request, *args, **kwargs)
