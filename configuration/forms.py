from django import forms
from .models import *


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        exclude = ('created_by', 'created_date', 'updated_by', 'updated_date',)
        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'}, ),
            "type": forms.TextInput(attrs={'class': 'form-control'}, ),
        }


class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = '__all__'
        exclude = ('created_by', 'created_date', 'updated_by', 'updated_date',)
        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control'}, ),
            "rate": forms.NumberInput(attrs={'class': 'form-control'}, ),
        }
