from django.db import models
from auditlog.registry import auditlog


class Category(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    created_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.IntegerField(blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'C_CATEGORY'


class Discount(models.Model):
    name = models.CharField(max_length=100)
    rate = models.FloatField()
    created_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.IntegerField(blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'C_DISCOUNT'


auditlog.register(Category)
auditlog.register(Discount)
