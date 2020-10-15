from django.db import models
from configuration.models import *
from account.models import Customer, Supplier


SIZE_CHOICES = (
    ("Small", 'Small'),
    ("Medium", 'Medium'),
    ("Large", 'Large'),
)


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.CharField(max_length=20, blank=True, null=True)
    size = models.CharField(choices=SIZE_CHOICES, max_length=6)
    price = models.FloatField()
    quantity_left = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    image = models.FileField(null=True, blank=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.IntegerField(blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + " (" + self.size + ")"

    class Meta:
        db_table = 'I_PRODUCT'


class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    expiry_date = models.DateTimeField(blank=True, null=True)
    buying_price = models.FloatField()
    quantity = models.IntegerField()
    total_price = models.FloatField(default=0.0)
    description = models.TextField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.IntegerField(blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name

    def get_total(self):
        total = self.buying_price * self.quantity
        return total

    class Meta:
        db_table = 'I_STOCK'


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField()
    net_total = models.FloatField(default=0.0)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    ordered_date = models.DateField()
    shipping_address = models.CharField(max_length=100, blank=True, null=True)
    billing_address = models.CharField(max_length=100, blank=True, null=True)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, blank=True, null=True)
    # is_tax_payable = models.BooleanField(default=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.IntegerField(blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name

    def get_total(self):
        total = self.product.price * self.quantity
        if self.discount:
            total -= (total * (self.discount.rate/100))
        # if self.is_tax_payable == True:
        #     total += (total * (15/100))
        return total

    class Meta:
        db_table = 'I_ORDER'
