from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,
    PermissionsMixin, Group)
from auditlog.registry import auditlog


TAG_CHOICE = (
    ("View", 'View'),
    ("Add", 'Add'),
    ("Edit", 'Edit'),
    ("Delete", 'Delete'),
)


class User_Manager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have a username')
        user = self.model(
            username=username,
            password=password,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            username,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Role(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.IntegerField(blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'A_ROLE'


class Users(models.Model):
    active_or_not = [(1, 'Yes'), (0, 'No')]

    name = models.CharField(max_length=50, blank=False)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=250, null=True, blank=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    ip_address = models.CharField(max_length=30, unique=True, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True, choices=active_or_not)
    last_login = models.DateTimeField(null=True, blank=True)
    language = models.CharField(max_length=10, default="Eng")
    created_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.IntegerField(blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True)

    objects = User_Manager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']

    class Meta:
        db_table = 'A_USERS'

    def __str__(self):
        return self.username


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=250, null=True, blank=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.IntegerField(blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'A_CUSTOMER'


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=250, null=True, blank=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.IntegerField(blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'A_SUPPLIER'


class Menu(models.Model):
    name = models.CharField(max_length=300)
    created_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.IntegerField(blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'A_MENU'


class Module(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    created_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.IntegerField(blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'A_MODULE'


class URL(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    url = models.CharField(max_length=300)
    tag = models.CharField(max_length=6, choices=TAG_CHOICE)
    created_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.IntegerField(blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.url

    class Meta:
        db_table = 'A_URL'


class Privilege(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    url = models.ForeignKey(URL, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    role_type = models.IntegerField(default=0)
    created_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.IntegerField(blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'A_PRIVILEGE'


auditlog.register(Role)
auditlog.register(Users)
auditlog.register(Customer)
auditlog.register(Supplier)
auditlog.register(Menu)
auditlog.register(Module)
auditlog.register(URL)
auditlog.register(Privilege)
