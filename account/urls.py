from django.urls import path
from .views import *

app_name = 'account'

urlpatterns = [
    path('', login, name='login'),
    path('signup/', login, name='login'),
    path('jk34BB23BHddv12HsNNJ/', login_validate, name='login_validate'),
    path('index/', index, name='index'),

    # path('forgotPassword/', forgot_password, name='forgot_password'),
    path('logout/', logout, name='logout'),

    path('register/', register, name='register'),
    path('usersList/', users_list, name='users_list'),
    path('userDelete/<int:id>', users_delete, name='users_delete'),

    path('rolesList/', roles_list, name='roles_list'),
    path('rolesAdd/', roles_process, name='roles_add'),
    path('rolesEdit/<int:id>', roles_process, name='roles_edit'),
    path('rolesDelete/<int:id>', roles_delete, name='roles_delete'),

    path('customerList/', customer_list, name='customer_list'),
    path('customerAdd/', customer_process, name='customer_add'),
    path('customerEdit/<int:id>', customer_process, name='customer_edit'),
    path('customerDelete/<int:id>', customer_delete, name='customer_delete'),

    path('supplierList/', supplier_list, name='supplier_list'),
    path('supplierAdd/', supplier_process, name='supplier_add'),
    path('supplierEdit/<int:id>', supplier_process, name='supplier_edit'),
    path('supplierDelete/<int:id>', supplier_delete, name='supplier_delete'),

    path('menusList/', menus_list, name='menus_list'),
    path('menusAdd/', menus_process, name='menus_add'),
    path('menusEdit/<int:id>', menus_process, name='menus_edit'),
    path('menusDelete/<int:id>', menus_delete, name='menus_delete'),

    path('modulesList/', modules_list, name='modules_list'),
    path('modulesAdd/', modules_process, name='modules_add'),
    path('modulesEdit/<int:id>', modules_process, name='modules_edit'),
    path('modulesDelete/<int:id>', modules_delete, name='modules_delete'),

    path('urlsList/', urls_list, name='urls_list'),
    path('urlsAdd/', urls_process, name='urls_add'),
    path('urlsEdit/<int:id>', urls_process, name='urls_edit'),
    path('urlsDelete/<int:id>', urls_delete, name='urls_delete'),

    path('privilege/<int:id>', privilege_list, name='privilege_list'),
    # path('groupPrivilege/<int:id>', group_privilege_list, name='group_privilege_list'),

]
