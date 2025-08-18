from django import forms
from .models import Farmer

class FarmerForm(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = ['name', 'farmer_type', 'phone', 'email', 'province', 'district', 'ward', 'address', 'total_farm_area', 'active_farm_area', 'farming_experience', 'main_crops', 'certifications']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập tên nông dân hoặc tổ chức'}),
            'farmer_type': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+84xxxxxxxxx'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'province': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'VD: Hà Nội'}),
            'district': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'VD: Hoàn Kiếm'}),
            'ward': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'VD: Hàng Bài'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Địa chỉ chi tiết'}),
            'total_farm_area': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'active_farm_area': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'farming_experience': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'main_crops': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'VD: Rau cải, cà chua, khoai tây'}),
            'certifications': forms.Select(attrs={'class': 'form-control'}),
        }

class FarmerUpdateForm(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = ['name', 'farmer_type', 'phone', 'email', 'province', 'district', 'ward', 'address', 'total_farm_area', 'active_farm_area', 'farming_experience', 'main_crops', 'certifications', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'farmer_type': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'province': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'ward': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'total_farm_area': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'active_farm_area': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'farming_experience': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'main_crops': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'certifications': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
