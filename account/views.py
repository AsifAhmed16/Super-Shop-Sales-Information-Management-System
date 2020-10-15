from django.http import HttpResponseRedirect, HttpResponse
import hashlib
from django.shortcuts import get_object_or_404
from datetime import datetime
from .forms import *
from .decorators import *
from items.models import Product


@login_required("logged_in", 'account:login')
def index(request):
    items = Product.objects.all().order_by('name')
    display = [{
        'id': x.id,
        'name': x.name,
        'price': x.price,
        'category': x.category.name,
        'brand': x.brand,
        'size': x.size,
        'image': (x.image).decode('utf-8'),
    } for x in items]
    context = dict()
    context['display'] = display
    lang = "Eng"
    if request.method == 'POST':
        items = Product.objects.filter(name__icontains=request.POST['Search']).order_by('name')
        display = [{
            'id': x.id,
            'name': x.name,
            'price': x.price,
            'category': x.category.name,
            'brand': x.brand,
            'size': x.size,
            'image': (x.image).decode('utf-8'),
        } for x in items]
        context['display'] = display
        context['search_text'] = request.POST['Search']
        if request.POST['language']:
            request.session['language'] = request.POST['language']
            userdata = {
                'language': request.POST['language'],
            }
            context['data'] = userdata
            if 'logged_in' in request.session:
                if request.session['logged_in'] is True:
                    userdata = {
                        'username': request.session['username'],
                        'logged_in': request.session['logged_in'],
                        'language': request.session['language'],
                    }
                    context['data'] = userdata
            return HttpResponseRedirect(request.path_info)
    if 'logged_in' in request.session:
        if request.session['logged_in'] is True:
            if 'language' in request.session:
                lang = request.session['language']
            else:
                request.session['language'] = lang
            userdata = {
                'username': request.session['username'],
                'logged_in': request.session['logged_in'],
                'language': lang,
            }
            context['data'] = userdata
    return render(request, 'account/home.html', context)


def login(request):
    if 'language' in request.session:
        userdata = {
            'language': request.session['language'],
        }
    else:
        request.session['language'] = "Eng"
        userdata = {
            'language': "Eng",
        }
    context = {
        'data': userdata
    }
    if 'logged_in' in request.session:
        if request.session['logged_in'] is True:
            return redirect('account:index')
    return render(request, 'account/login.html', context)


def login_validate(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = hashlib.sha256(request.POST['password'].encode('utf-8')).hexdigest()
        try:
            user = Users.objects.get(username=username)
        except Exception as ex:
            user = None
        if user is None:
            if request.session['language'] == "Eng":
                    messages.error(request, 'Username Mismatched')
            else:
                messages.error(request, 'ব্যবহারকারী আইডি মিলছে না')
            return redirect('account:login')
        else:
            if user.password == password:
                request.session['logged_in'] = True
                request.session['username'] = user.username
                request.session['id'] = user.pk
                request.session['language'] = user.language
                user.last_login = datetime.now()
                user.save()
                privilege_urls = Privilege.objects.filter(user_id=user.pk)
                url_list = []
                for each in privilege_urls:
                    urls = URL.objects.filter(id=each.url_id).values_list('url', flat=True)
                    url_list.extend(urls)
                request.session['urls'] = url_list

                return redirect("account:index")
            else:
                if request.session['language'] == "Eng":
                    messages.error(request, 'Wrong Password')
                else:
                    messages.error(request, 'ভুল গোপন নম্বর')
                return redirect('account:login')
    return render(request, 'account/login.html')


def register(request):
    if 'language' in request.session:
        userdata = {
            'language': request.session['language'],
        }
    else:
        request.session['language'] = "Eng"
        userdata = {
            'language': "Eng",
        }
    all_roles = Role.objects.all()
    context = {
        'data': userdata,
        'roles_list': all_roles
    }
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_again = request.POST['password-again']
        email = request.POST['email']
        role = Role.objects.get(id=request.POST['role'])
        name = request.POST['name']
        location = request.POST['location']
        phone = request.POST['phone']
        if password != password_again:
            if request.session['language'] == "Eng":
                messages.error(request, 'Password Mismatched. Try Again')
            else:
                messages.error(request, 'পাসওয়ার্ড মেলেনি. আবার চেষ্টা করুন')
            return redirect('account:register')
        try:
            if Users.objects.filter(username=username).exists():
                if request.session['language'] == "Eng":
                    messages.error(request, 'That username is already taken.')
                else:
                    messages.error(request, 'এই ব্যবহারকারীর নামটি ইতিমধ্যে নেওয়া হয়েছে')
                return redirect('account:register')
            if Users.objects.filter(email=email).exists():
                if request.session['language'] == "Eng":
                    messages.error(request, 'That email id is already taken.')
                else:
                    messages.error(request, 'এই ইমেলটি ইতিমধ্যে নেওয়া হয়েছে')
                return redirect('account:register')
            password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            Users.objects.create(username=username, password=password, email=email, name=name, location=location, phone=phone, role=role, is_active=1, language=request.session['language'])
            if request.session['language'] == "Eng":
                messages.success(request, 'Registration Complete.')
            else:
                messages.success(request, 'নিবন্ধন সম্পন্ন.')
        except Exception as ex:
            print(ex)
            if request.session['language'] == "Eng":
                messages.error(request, 'Sorry !!! Something Went Wrong.')
            else:
                messages.error(request, 'দুঃখিত !!! কিছু ভুল হয়েছে')
            return redirect('account:register')
        return redirect('account:login')
    else:
        return render(request, 'account/register.html', context)


def logout(request):
    try:
        del request.session['logged_in']
        return redirect('account:login')
    except:
        return redirect('account:login')


def users_list(request):
    try:
        userdata = {
            'user_id': request.session['id'],
            'username': request.session['username'],
            'language': request.session['language'],
            'urls': request.session['urls'],
        }
        users = Users.objects.all().order_by('name')
        context = {
            'data': userdata,
            'items': users,
        }
        return render(request, 'account/users_list.html', context)
    except Exception as ex:
        messages.error(request, str(ex))
        return redirect('account:index')


@login_required("logged_in", 'account:login')
@access_permission_required
def users_delete(request, id):
    Users.objects.get(pk=id).delete()
    messages.error(request, 'Data Deleted')
    return redirect('account:users_list')


# Role Module
def roles_list(request):
    try:
        language = "Eng"
        if 'language' in request.session:
            language = request.session['language']
        userdata = {
            'user_id': request.session['id'],
            'username': request.session['username'],
            'language': language,
            'urls': request.session['urls'],
        }
        roles = Role.objects.all()
        context = {
            'data': userdata,
            'items': roles,
        }
        return render(request, 'account/roles_list.html', context)
    except Exception as ex:
        messages.error(request, str(ex))
        return redirect('account:index')


@login_required("logged_in", 'account:login')
@access_permission_required
def roles_process(request, id=None):
    try:
        form = RolesForm
        userdata = {
            'user_id': request.session['id'],
            'username': request.session['username'],
            'language': request.session['language'],
            'urls': request.session['urls'],
        }
        context = dict()
        context['data'] = userdata
        context['form'] = form

        if request.method == 'POST' and id:
            roleobj = get_object_or_404(Role, pk=id)
            form = RolesForm(request.POST or None, instance=roleobj)
            if form.is_valid():
                editform = form.save(commit=False)
                editform.updated_by = request.session['id']
                editform.updated_date = datetime.now()
                editform.save()
                messages.success(request, 'Data Successfully Updated')
                return redirect('account:roles_list')
        elif id:
            roleobj = get_object_or_404(Role, pk=id)
            form = RolesForm(request.POST or None, instance=roleobj)
            context['form'] = form
        elif request.method == 'POST':
            form = RolesForm(request.POST, request.FILES or None)
            if form.is_valid():
                process_area = form.save(commit=False)
                process_area.created_date = datetime.now()
                process_area.created_by = request.session['id']
                process_area.save()
                messages.success(request, 'Data Successfully Saved')
                return redirect('account:roles_list')
            else:
                context = {
                    'data': userdata,
                    'form': form
                }
                return render(request, 'account/roles_form.html', context)
        return render(request, 'account/roles_form.html', context)
    except Exception as ex:
        messages.error(request, str(ex))
        return redirect('account:roles_list')


@login_required("logged_in", 'account:login')
@access_permission_required
def roles_delete(request, id):
    Role.objects.get(pk=id).delete()
    messages.error(request, 'Data Deleted')
    return redirect('account:roles_list')


# Customer Module
def customer_list(request):
    try:
        language = "Eng"
        if 'language' in request.session:
            language = request.session['language']
        userdata = {
            'user_id': request.session['id'],
            'username': request.session['username'],
            'language': language,
            'urls': request.session['urls'],
        }
        items = Customer.objects.all()
        context = {
            'data': userdata,
            'items': items,
        }
        return render(request, 'account/customer_list.html', context)
    except Exception as ex:
        messages.error(request, str(ex))
        return redirect('account:index')


@login_required("logged_in", 'account:login')
@access_permission_required
def customer_process(request, id=None):
    try:
        form = CustomerForm
        userdata = {
            'user_id': request.session['id'],
            'username': request.session['username'],
            'language': request.session['language'],
            'urls': request.session['urls'],
        }
        context = dict()
        context['data'] = userdata
        context['form'] = form

        if request.method == 'POST' and id:
            obj = get_object_or_404(Customer, pk=id)
            form = CustomerForm(request.POST or None, instance=obj)
            if form.is_valid():
                editform = form.save(commit=False)
                editform.updated_by = request.session['id']
                editform.updated_date = datetime.now()
                editform.save()
                messages.success(request, 'Data Updated')
                return redirect('account:customer_list')
        elif id:
            obj = get_object_or_404(Customer, pk=id)
            form = CustomerForm(request.POST or None, instance=obj)
            context['form'] = form
        elif request.method == 'POST':
            form = CustomerForm(request.POST, request.FILES or None)
            if form.is_valid():
                process_area = form.save(commit=False)
                process_area.created_date = datetime.now()
                process_area.created_by = request.session['id']
                process_area.save()
                messages.success(request, 'Data Successfully Saved')
                return redirect('account:customer_list')
            else:
                context = {
                    'data': userdata,
                    'form': form
                }
                return render(request, 'account/customer_form.html', context)
        return render(request, 'account/customer_form.html', context)
    except Exception as ex:
        messages.error(request, str(ex))
        return redirect('account:customer_list')


@login_required("logged_in", 'account:login')
@access_permission_required
def customer_delete(request, id):
    Customer.objects.get(pk=id).delete()
    messages.error(request, 'Data Deleted')
    return redirect('account:customer_list')


# Supplier Module
def supplier_list(request):
    try:
        language = "Eng"
        if 'language' in request.session:
            language = request.session['language']
        userdata = {
            'user_id': request.session['id'],
            'username': request.session['username'],
            'language': language,
            'urls': request.session['urls'],
        }
        items = Supplier.objects.all()
        context = {
            'data': userdata,
            'items': items,
        }
        return render(request, 'account/supplier_list.html', context)
    except Exception as ex:
        messages.error(request, str(ex))
        return redirect('account:index')


@login_required("logged_in", 'account:login')
@access_permission_required
def supplier_process(request, id=None):
    try:
        form = SupplierForm
        userdata = {
            'user_id': request.session['id'],
            'username': request.session['username'],
            'language': request.session['language'],
            'urls': request.session['urls'],
        }
        context = dict()
        context['data'] = userdata
        context['form'] = form

        if request.method == 'POST' and id:
            obj = get_object_or_404(Supplier, pk=id)
            form = SupplierForm(request.POST or None, instance=obj)
            if form.is_valid():
                editform = form.save(commit=False)
                editform.updated_by = request.session['id']
                editform.updated_date = datetime.now()
                editform.save()
                messages.success(request, 'Data Updated')
                return redirect('account:supplier_list')
        elif id:
            obj = get_object_or_404(Supplier, pk=id)
            form = SupplierForm(request.POST or None, instance=obj)
            context['form'] = form
        elif request.method == 'POST':
            form = SupplierForm(request.POST, request.FILES or None)
            if form.is_valid():
                process_area = form.save(commit=False)
                process_area.created_date = datetime.now()
                process_area.created_by = request.session['id']
                process_area.save()
                messages.success(request, 'Data Successfully Saved')
                return redirect('account:supplier_list')
            else:
                context = {
                    'data': userdata,
                    'form': form
                }
                return render(request, 'account/supplier_form.html', context)
        return render(request, 'account/supplier_form.html', context)
    except Exception as ex:
        messages.error(request, str(ex))
        return redirect('account:supplier_list')


@login_required("logged_in", 'account:login')
@access_permission_required
def supplier_delete(request, id):
    Supplier.objects.get(pk=id).delete()
    messages.error(request, 'Data Deleted')
    return redirect('account:supplier_list')


# Menu Module
def menus_list(request):
    try:
        userdata = {
            'user_id': request.session['id'],
            'username': request.session['username'],
            'language': request.session['language'],
            'urls': request.session['urls'],
        }
        items = Menu.objects.all().order_by('name')
        context = {
            'data': userdata,
            'items': items
        }
        return render(request, 'account/menus_list.html', context)
    except Exception as ex:
        messages.error(request, str(ex))
        return redirect('account:index')


@login_required("logged_in", 'account:login')
@access_permission_required
def menus_process(request, id=None):
    try:
        form = MenusForm
        userdata = {
            'user_id': request.session['id'],
            'username': request.session['username'],
            'language': request.session['language'],
            'urls': request.session['urls'],
        }
        context = {
            'data': userdata,
            'form': form
        }
        if request.method == 'POST' and id:
            item = get_object_or_404(Menu, pk=id)
            form = MenusForm(request.POST or None, instance=item)

            if form.is_valid():
                form = form.save(commit=False)
                form.updated_by = request.session['id']
                form.updated_date = datetime.now()
                form.save()
                messages.success(request, 'Data Updated')
                return redirect('account:menus_list')
        elif id:
            item = get_object_or_404(Menu, pk=id)
            form = MenusForm(request.POST or None, instance=item)
            context['form'] = form
        elif request.method == 'POST':
            form = MenusForm(request.POST, request.FILES or None)
            if form.is_valid():
                form = form.save(commit=False)
                form.created_by = request.session['id']
                form.created_date = datetime.now()
                form.save()
                messages.success(request, 'Data Saved')
                return redirect('account:menus_list')
            else:
                context = {
                    'data': userdata,
                    'form': form
                }
                return render(request, 'account/menus_form.html', context)
        return render(request, 'account/menus_form.html', context)
    except Exception as ex:
        messages.error(request, str(ex))
        return redirect('account:menus_list')


@login_required("logged_in", 'account:login')
@access_permission_required
def menus_delete(request, id):
    Menu.objects.get(pk=id).delete()
    messages.error(request, 'Data Deleted')
    return redirect('account:menus_list')


# Module List Module
def modules_list(request):
    try:
        userdata = {
            'user_id': request.session['id'],
            'username': request.session['username'],
            'language': request.session['language'],
            'urls': request.session['urls'],
        }
        items = Module.objects.all().order_by('menu')
        context = {
            'data': userdata,
            'items': items
        }
        return render(request, 'account/modules_list.html', context)
    except Exception as ex:
        messages.error(request, str(ex))
        return redirect('account:index')


@login_required("logged_in", 'account:login')
@access_permission_required
def modules_process(request, id=None):
    try:
        form = ModulesForm
        userdata = {
            'user_id': request.session['id'],
            'username': request.session['username'],
            'language': request.session['language'],
            'urls': request.session['urls'],
        }
        context = {
            'data': userdata,
            'form': form
        }
        if request.method == 'POST' and id:
            item = get_object_or_404(Module, pk=id)
            form = ModulesForm(request.POST or None, instance=item)

            if form.is_valid():
                form = form.save(commit=False)
                form.updated_by = request.session['id']
                form.updated_date = datetime.now()
                form.save()
                messages.success(request, 'Data Updated')
                return redirect('account:modules_list')
        elif id:
            item = get_object_or_404(Module, pk=id)
            form = ModulesForm(request.POST or None, instance=item)
            context['form'] = form
        elif request.method == 'POST':
            form = ModulesForm(request.POST, request.FILES or None)
            if form.is_valid():
                form = form.save(commit=False)
                form.created_by = request.session['id']
                form.created_date = datetime.now()
                form.save()
                messages.success(request, 'Data Saved')
                return redirect('account:modules_list')
            else:
                context = {
                    'data': userdata,
                    'form': form
                }
                return render(request, 'account/modules_form.html', context)
        return render(request, 'account/modules_form.html', context)
    except Exception as ex:
        messages.error(request, str(ex))
        return redirect('account:modules_list')


@login_required("logged_in", 'account:login')
@access_permission_required
def modules_delete(request, id):
    Module.objects.get(pk=id).delete()
    messages.error(request, 'Data Deleted')
    return redirect('account:modules_list')


# Urls Module
def urls_list(request):
    try:
        userdata = {
            'user_id': request.session['id'],
            'username': request.session['username'],
            'language': request.session['language'],
            'urls': request.session['urls'],
        }
        items = URL.objects.all().order_by('module_id')
        context = {
            'data': userdata,
            'items': items
        }
        return render(request, 'account/urls_list.html', context)
    except Exception as ex:
        messages.error(request, str(ex))
        return redirect('account:index')


@login_required("logged_in", 'account:login')
@access_permission_required
def urls_process(request, id=None):
    try:
        form = URLSForm
        userdata = {
            'user_id': request.session['id'],
            'username': request.session['username'],
            'language': request.session['language'],
            'urls': request.session['urls'],
        }
        context = {
            'data': userdata,
            'form': form
        }
        if request.method == 'POST' and id:
            item = get_object_or_404(URL, pk=id)
            form = URLSForm(request.POST or None, instance=item)
            if form.is_valid():
                form = form.save(commit=False)
                form.updated_by = request.session['id']
                form.updated_date = datetime.now()
                form.save()
                messages.success(request, 'Data Updated')
                return redirect('account:urls_list')
        elif id:
            item = get_object_or_404(URL, pk=id)
            form = URLSForm(request.POST or None, instance=item)
            context['form'] = form
        elif request.method == 'POST':
            form = URLSForm(request.POST, request.FILES or None)
            if form.is_valid():
                form = form.save(commit=False)
                form.created_by = request.session['id']
                form.created_date = datetime.now()
                form.save()
                messages.success(request, 'Data Saved')
                return redirect('account:urls_list')
            else:
                context = {
                    'data': userdata,
                    'form': form
                }
                return render(request, 'account/urls_form.html', context)
        return render(request, 'account/urls_form.html', context)
    except Exception as ex:
        messages.error(request, str(ex))
        return redirect('account:urls_list')


@login_required("logged_in", 'account:login')
@access_permission_required
def urls_delete(request, id):
    URL.objects.get(pk=id).delete()
    messages.error(request, 'Data Deleted')
    return redirect('account:urls_list')


@login_required("logged_in", 'account:login')
@access_permission_required
def privilege_list(request, id):
    try:
        userdata = {
            'user_id': request.session['id'],
            'username': request.session['username'],
            'language': request.session['language'],
            'urls': request.session['urls'],
        }
        menus = Menu.objects.all()
        modules = Module.objects.all()
        urls = URL.objects.all()
        privileges = Privilege.objects.filter(user=id).order_by('module_id')
        user_obj = Users.objects.get(id=id)
        role_obj = get_object_or_404(Role, pk=user_obj.role.id)
        context = {
            'data': userdata,
            'menus': menus,
            'modules': modules,
            'urls': urls,
            'privileges': privileges,
        }

        if request.method == 'POST':
            privilege_list = request.POST.getlist('list')
            Privilege.objects.filter(user_id=id).delete()
            for data in privilege_list:
                data = data.split(',')
                Privilege.objects.create(user_id=id, role=role_obj, menu_id=data[0], module_id=data[1],
                                         url_id=data[2],
                                         created_by=request.session['id'], created_date=(datetime.now()))
            messages.success(request, 'Data Saved Successfully')
            return redirect('account:users_list')
        return render(request, 'account/privilege.html', context)

    except Exception as ex:
        messages.error(request, str(ex))
        return redirect('account:index')


# @login_required("logged_in", 'account:login')
# @access_permission_required
# def group_privilege_list(request, id):
#     try:
#         if 'logged_in' in request.session:
#             if request.session['logged_in'] is True:
#                 userdata = {
#                     'user_id': request.session['id'],
#                     'username': request.session['username'],
#                 }
#                 modules = Module.objects.all()
#                 urls = URL.objects.all()
#                 privileges = Privilege.objects.filter(role=id).order_by('module')
#                 context = {
#                     'data': userdata,
#                     'modulelall': modules,
#                     'moduleurl': urls,
#                     'privileged': privileges,
#                 }
#                 if request.method == 'POST':
#                     list = request.POST.getlist('list')
#                     Privilege.objects.filter(user_id=None, role_id=id).delete()
#                     role_obj = get_object_or_404(Role, pk=id)
#                     for data in list:
#                         data = data.split(',')
#                         Privilege.objects.create(role=role_obj, menu_id=data[0], module_id=data[1], url_id=data[2],
#                                                   created_by=request.session['id'], created_date=(datetime.now()))
#                     messages.success(request, 'Data Saved Successfully')
#                     return redirect('account:roles_list')
#                 return render(request, 'account/privilege_group.html', context)
#         else:
#             return redirect('account:login')
#     except Exception as ex:
#         messages.error(request, str(ex))
#         return redirect('account:index')
