from django import forms
from .models import *


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ('image', 'created_by', 'created_date', 'updated_by', 'updated_date',)
        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'}, ),
            "brand": forms.TextInput(attrs={'class': 'form-control'}, ),
            "size": forms.Select(attrs={'class': 'select '}),
            "price": forms.NumberInput(attrs={'class': 'form-control'}, ),
            "category": forms.Select(attrs={'class': 'select '}),
            "description": forms.Textarea(attrs={'class': 'form-control'}),
        }


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = '__all__'
        exclude = ('total_price', 'created_by', 'created_date', 'updated_by', 'updated_date',)
        widgets = {
            "product": forms.Select(attrs={'class': 'select '}),
            "supplier": forms.Select(attrs={'class': 'select '}),
            "quantity": forms.NumberInput(attrs={'class': 'form-control'}, ),
            "buying_price": forms.NumberInput(attrs={'class': 'form-control'}, ),
            "description": forms.Textarea(attrs={'class': 'form-control'}),
            "expiry_date": forms.DateInput(attrs={'class': 'form-control', 'type': 'text', 'id': 'datepicker'}),
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ('net_total', 'created_by', 'created_date', 'updated_by', 'updated_date')
        widgets = {
            "customer": forms.Select(attrs={'class': 'select '}),
            "product": forms.Select(attrs={'class': 'select '}),
            "quantity": forms.NumberInput(attrs={'class': 'form-control'}, ),
            "ref_code": forms.TextInput(attrs={'class': 'form-control'}, ),
            "ordered_date": forms.DateInput(attrs={'class': 'form-control', 'type': 'text', 'id': 'datepicker'}),
            "shipping_address": forms.TextInput(attrs={'class': 'form-control'}, ),
            "billing_address": forms.TextInput(attrs={'class': 'form-control'}, ),
            "discount": forms.Select(attrs={'class': 'select '}),
        }
