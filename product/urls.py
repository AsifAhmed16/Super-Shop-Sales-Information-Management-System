from django.urls import path
from .views import *

app_name = 'product'

urlpatterns = [
    path('productList/', product_list, name='product_list'),
    path('productAdd/', product_process, name='product_add'),
    path('productEdit/<int:id>', product_process, name='product_edit'),
    path('productDelete/<int:id>', product_delete, name='product_delete'),
]
