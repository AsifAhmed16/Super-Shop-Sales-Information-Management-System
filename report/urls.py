from django.urls import path
from .views import *

app_name = 'report'

urlpatterns = [
    path('customer_report', customer_report, name='customer_report'),
    path('export_customer_report', export_customer_report, name='export_customer_report'),

    path('supplier_report', supplier_report, name='supplier_report'),
    path('export_supplier_report', export_supplier_report, name='export_supplier_report'),

    path('product_report', product_report, name='product_report'),
    path('export_product_report', export_product_report, name='export_product_report'),

    path('stock_report', stock_report, name='stock_report'),
    path('export_stock_report', export_stock_report, name='export_stock_report'),

    path('sales_report', sales_report, name='sales_report'),
    path('export_sales_report', export_sales_report, name='export_sales_report'),

    path('profit_loss_report', profit_loss_report, name='profit_loss_report'),
    path('export_profit_loss_report', export_profit_loss_report, name='export_profit_loss_report'),
]
