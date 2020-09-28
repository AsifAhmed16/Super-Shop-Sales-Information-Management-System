from django.urls import path
from .views import *

app_name = 'configuration'

urlpatterns = [
    # Category
    path('category/', CategoryListView.as_view(), name='CategoryListView'),
    path('category/add/', CategoryCreateView.as_view(), name='CategoryCreateView'),
    path('category/edit/<int:pk>/', CategoryUpdateView.as_view(), name='CategoryUpdateView'),
    path('category/delete/<int:id>/', CategoryDeleteView, name='CategoryDeleteView'),

    # Discount
    path('discount/', DiscountListView.as_view(), name='DiscountListView'),
    path('discount/add/', DiscountCreateView.as_view(), name='DiscountCreateView'),
    path('discount/edit/<int:pk>/', DiscountUpdateView.as_view(), name='DiscountUpdateView'),
    path('discount/delete/<int:id>/', DiscountDeleteView, name='DiscountDeleteView'),
]
