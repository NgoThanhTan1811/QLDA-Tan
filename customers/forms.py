from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['full_name', 'phone', 'email', 'province', 'district', 'ward', 'address', 'is_active']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập họ tên đầy đủ'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+84xxxxxxxxx'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'province': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'VD: Hà Nội'}),
            'district': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'VD: Hoàn Kiếm'}),
            'ward': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'VD: Hàng Bài'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Địa chỉ chi tiết'}),
        }

class CustomerUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['full_name', 'phone', 'email', 'province', 'district', 'ward', 'address', 'is_active']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'province': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'ward': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
