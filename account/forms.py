from django import forms
from .models import *


class RolesForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = '__all__'
        exclude = ('created_by', 'created_date', 'updated_by', 'updated_date',)
        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'}, ),
        }


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ('created_by', 'created_date', 'updated_by', 'updated_date',)
        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'}, ),
            "email": forms.TextInput(attrs={'class': 'form-control'}, ),
            "phone": forms.TextInput(attrs={'class': 'form-control'}, ),
        }


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'
        exclude = ('created_by', 'created_date', 'updated_by', 'updated_date',)
        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'}, ),
            "email": forms.TextInput(attrs={'class': 'form-control'}, ),
            "phone": forms.TextInput(attrs={'class': 'form-control'}, ),
        }


class MenusForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = '__all__'
        exclude = ('created_by', 'created_date', 'updated_by', 'updated_date',)
        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'}, ),
        }


class ModulesForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = '__all__'
        exclude = ('created_by', 'created_date', 'updated_by', 'updated_date',)
        widgets = {
            "menu": forms.Select(attrs={'class': 'select'}),
            "name": forms.TextInput(attrs={'class': 'form-control'}),
        }


class URLSForm(forms.ModelForm):
    class Meta:
        model = URL
        fields = '__all__'
        exclude = ('created_by', 'created_date', 'updated_by', 'updated_date',)
        widgets = {
            "menu": forms.Select(attrs={'class': 'select'}),
            "module": forms.Select(attrs={'class': 'form-control'}),
            "url": forms.TextInput(attrs={'class': 'form-control'}, ),
            "tag": forms.Select(attrs={'class': 'select'}),
        }
