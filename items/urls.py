from django.urls import path
from .views import *

app_name = 'items'

urlpatterns = [
    # Product
    path('product/', ProductListView.as_view(), name='ProductListView'),
    path('product/add/', ProductCreateView.as_view(), name='ProductCreateView'),
    path('product/details/<int:id>/', ProductDetailsView, name='ProductDetailsView'),
    path('product/edit/<int:id>/', ProductUpdateView, name='ProductUpdateView'),
    path('product/delete/<int:id>/', ProductDeleteView, name='ProductDeleteView'),

    # Stock
    path('stock/', StockListView.as_view(), name='StockListView'),
    path('stock/add/', StockCreateView.as_view(), name='StockCreateView'),
    # path('stock/edit/<int:id>/', StockUpdateView, name='StockUpdateView'),
    # path('stock/delete/<int:id>/', StockDeleteView, name='StockDeleteView'),

    # Order
    path('order/', OrderListView.as_view(), name='OrderListView'),
    path('order/create/<int:id>/', OrderCreate, name='OrderCreate'),
    path('order/add/', OrderCreateView, name='OrderCreateView'),
    # path('order/edit/<int:pk>/', OrderUpdateView.as_view(), name='OrderUpdateView'),
    # path('order/delete/<int:id>/', OrderDeleteView, name='OrderDeleteView'),

    path('check_img/<product_id>/', check_img, name='check_img'),

]
