from .forms import *
from django.urls import reverse_lazy
from account.decorators import *
from django.views.generic import ListView, CreateView, UpdateView
from datetime import datetime
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import socket
# from .tasks import send_task_mail


@method_decorator(login_required("logged_in", 'account:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class ProductListView(ListView):
    model = Product
    template_name = 'items/product_list.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'language': self.request.session['language'],
            'urls': self.request.session['urls'],
        }
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['data'] = userdata
        return context


@method_decorator(login_required("logged_in", 'account:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'items/product_form.html'
    success_url = reverse_lazy('items:ProductListView')

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'language': self.request.session['language'],
            'urls': self.request.session['urls'],
        }
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['form'] = self.form_class
        return context

    def form_valid(self, form):
        if form.is_valid:
            item = form.save(commit=False)
            if Product.objects.filter(name=self.request.POST['name'],
                                      brand=self.request.POST['brand'],
                                      size=self.request.POST['size']).exists():
                messages.error(self.request, 'Product Already Exists.')
                return super(ProductListView, self).form_invalid(form)
            item.image = self.request.POST['b64']
            item.created_date = datetime.today()
            item.created_by = self.request.session['id']
            item.save()
            messages.success(self.request, 'Data Successfully Saved')
            return super(ProductCreateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(ProductCreateView, self).form_invalid(form)


def ProductDetailsView(request, id):
    try:
        userdata = {
            'user_id': request.session['id'],
            'username': request.session['username'],
            'language': request.session['language'],
            'urls': request.session['urls'],
        }
        item_obj = get_object_or_404(Product, pk=id)
        try:
            stock_obj = Stock.objects.filter(product_id=id).latest('id')
        except:
            stock_obj = None
        form = ProductForm(request.POST or None, instance=item_obj)
        context = dict()
        context['data'] = userdata
        img_text = item_obj.image
        context['src_image'] = img_text.decode('utf-8')
        context['item'] = item_obj
        context['stock_item'] = stock_obj
        if request.method == 'POST' and id:
            if form.is_valid():
                item = form.save(commit=False)
                item.updated_by = request.session['id']
                item.updated_date = datetime.now()
                if request.POST['b64'] != "":
                    item.image = request.POST['b64']
                else:
                    item.image = img_text.decode('utf-8')
                item.save()
                messages.success(request, 'Data Successfully Updated')
                return redirect('items:ProductListView')
        return render(request, 'items/product_details.html', context)
    except Exception as ex:
        messages.error(request, str(ex))
        return redirect('items:ProductListView')


@login_required("logged_in", 'account:login')
@access_permission_required
def ProductUpdateView(request, id):
    try:
        userdata = {
            'user_id': request.session['id'],
            'username': request.session['username'],
            'language': request.session['language'],
            'urls': request.session['urls'],
        }
        item_obj = get_object_or_404(Product, pk=id)
        form = ProductForm(request.POST or None, instance=item_obj)
        context = dict()
        context['data'] = userdata
        context['form'] = form
        img_text = item_obj.image
        context['src_image'] = img_text.decode('utf-8')

        if request.method == 'POST' and id:
            if form.is_valid():
                item = form.save(commit=False)
                if Product.objects.filter(name=request.POST['name'],
                                          brand=request.POST['brand'],
                                          size=request.POST['size']).exclude(id=id).exists():
                    messages.error(request, 'Product Already Exists.')
                    return redirect('items:ProductListView')
                item.updated_by = request.session['id']
                item.updated_date = datetime.now()
                if request.POST['b64'] != "":
                    item.image = request.POST['b64']
                else:
                    item.image = img_text.decode('utf-8')
                item.save()
                messages.success(request, 'Data Successfully Updated')
                return redirect('items:ProductListView')
        return render(request, 'items/product_form.html', context)
    except Exception as ex:
        messages.error(request, str(ex))
        return redirect('items:ProductListView')


@login_required("logged_in", 'account:login')
@access_permission_required
def ProductDeleteView(request, id):
    Product.objects.get(pk=id).delete()
    messages.error(request, 'Data Successfully Deleted')
    return redirect('items:ProductListView')


@method_decorator(login_required("logged_in", 'account:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class StockListView(ListView):
    model = Stock
    template_name = 'items/stock_list.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'language': self.request.session['language'],
            'urls': self.request.session['urls'],
        }
        context = super(StockListView, self).get_context_data(**kwargs)
        context['data'] = userdata
        return context


@method_decorator(login_required("logged_in", 'account:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class StockCreateView(CreateView):
    model = Stock
    form_class = StockForm
    template_name = 'items/stock_form.html'
    success_url = reverse_lazy('items:StockListView')

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'language': self.request.session['language'],
            'urls': self.request.session['urls'],
        }
        context = super(StockCreateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['form'] = self.form_class
        return context

    def form_valid(self, form):
        if form.is_valid:
            item = form.save(commit=False)
            item.total_price = item.get_total()
            item.created_date = datetime.today()
            item.created_by = self.request.session['id']
            product_obj = Product.objects.get(id=self.request.POST['product'])
            Product.objects.filter(id=self.request.POST['product']).update(quantity_left=int(product_obj.quantity_left) + int(self.request.POST['quantity']))
            item.save()
            messages.success(self.request, 'Data Successfully Saved')
            return super(StockCreateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(StockCreateView, self).form_invalid(form)


# @login_required("logged_in", 'account:login')
# @access_permission_required
# def StockUpdateView(request, id):
#     try:
#         userdata = {
#             'user_id': request.session['id'],
#             'username': request.session['username'],
#             'urls': request.session['urls'],
#         }
#         item_obj = get_object_or_404(Stock, pk=id)
#         form = StockForm(request.POST or None, instance=item_obj)
#         context = dict()
#         context['data'] = userdata
#         context['form'] = form
#         if request.method == 'POST' and id:
#             if form.is_valid():
#                 item = form.save(commit=False)
#                 item.total_price = item.get_total()
#                 item.updated_by = request.session['id']
#                 item.updated_date = datetime.now()
#                 item.save()
#                 messages.success(request, 'Data Successfully Updated')
#                 return redirect('items:StockListView')
#         return render(request, 'items/stock_form.html', context)
#     except Exception as ex:
#         messages.error(request, str(ex))
#         return redirect('items:StockListView')


# @login_required("logged_in", 'account:login')
# @access_permission_required
# def StockDeleteView(request, id):
#     Stock.objects.get(pk=id).delete()
#     messages.error(request, 'Data Successfully Deleted')
#     return redirect('items:StockListView')


@method_decorator(login_required("logged_in", 'account:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class OrderListView(ListView):
    model = Order
    template_name = 'items/order_list.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'language': self.request.session['language'],
            'urls': self.request.session['urls'],
        }
        context = super(OrderListView, self).get_context_data(**kwargs)
        context['data'] = userdata
        return context


# @login_required("logged_in", 'account:login')
# @access_permission_required
def OrderCreate(request, id):
    try:
        userdata = {
            'user_id': request.session['id'],
            'username': request.session['username'],
            'language': request.session['language'],
            'urls': request.session['urls'],
        }
        item_obj = get_object_or_404(Product, pk=id)
        context = dict()
        context['data'] = userdata
        data = {'product': item_obj}
        form = OrderForm(data)
        context['form'] = form
        img_code = item_obj.image
        img_code = img_code.decode('utf-8')
        context['src_image'] = img_code
        if request.method == 'POST':
            if int(item_obj.quantity_left) < int(request.POST['quantity']):
                messages.error(request, 'Product Quantity Exceed')
                return redirect('items:OrderListView')
            smonth, sday, syear = request.POST['ordered_date'].split('/')
            ordered_date = str(syear) + "-" + str(smonth) + "-" + str(sday)
            Order.objects.create(product_id=int(request.POST['product']),
                                 customer_id=int(request.POST['customer']),
                                 quantity=int(request.POST['quantity']),
                                 ref_code=request.POST['ref_code'],
                                 ordered_date=ordered_date,
                                 shipping_address=request.POST['shipping_address'],
                                 billing_address=request.POST['billing_address'],
                                 discount_id=int(request.POST['discount']),
                                 created_by=int(request.session['id']))
            Product.objects.filter(id=request.POST['product']).update(
                quantity_left=int(item_obj.quantity_left) - int(request.POST['quantity']))
            o_item = Order.objects.latest('id')
            Order.objects.filter(id=o_item.id).update(net_total=o_item.get_total())
            # mail_confirm_notification(self.request, Customer.objects.get(id=self.request.POST['customer']))
            messages.success(request, 'Data Successfully Saved')
            return redirect('items:OrderListView')
        return render(request, 'items/order_form.html', context)
    except Exception as ex:
        messages.error(request, str(ex))
        return redirect('items:OrderListView')


@login_required("logged_in", 'account:login')
@access_permission_required
def OrderCreateView(request):
    try:
        userdata = {
            'user_id': request.session['id'],
            'username': request.session['username'],
            'language': request.session['language'],
            'urls': request.session['urls'],
        }
        context = dict()
        context['data'] = userdata
        form = OrderForm()
        context['form'] = form
        # mail_confirm_notification(request, Customer.objects.get(id=2))
        if request.method == 'POST':
            item_obj = get_object_or_404(Product, pk=int(request.POST['product']))
            if int(item_obj.quantity_left) < int(request.POST['quantity']):
                messages.error(request, 'Product Quantity Exceed')
                return redirect('items:OrderListView')
            smonth, sday, syear = request.POST['ordered_date'].split('/')
            ordered_date = str(syear) + "-" + str(smonth) + "-" + str(sday)
            discount_id = None
            if request.POST['discount']:
                discount_id = int(request.POST['discount'])
            Order.objects.create(product_id=int(request.POST['product']),
                                 customer_id=int(request.POST['customer']),
                                 quantity=int(request.POST['quantity']),
                                 ref_code=request.POST['ref_code'],
                                 ordered_date=ordered_date,
                                 shipping_address=request.POST['shipping_address'],
                                 billing_address=request.POST['billing_address'],
                                 discount_id=discount_id,
                                 created_by=int(request.session['id']))
            Product.objects.filter(id=request.POST['product']).update(
                quantity_left=int(item_obj.quantity_left) - int(request.POST['quantity']))
            o_item = Order.objects.latest('id')
            Order.objects.filter(id=o_item.id).update(net_total=o_item.get_total())
            # mail_confirm_notification(request, Customer.objects.get(id=request.POST['customer']))
            messages.success(request, 'Data Successfully Saved')
            return redirect('items:OrderListView')
        return render(request, 'items/order_form.html', context)
    except Exception as ex:
        messages.error(request, str(ex))
        return redirect('items:OrderListView')


# @login_required("logged_in", 'account:login')
# @access_permission_required
# class OrderCreateView(request):
#     try:
#         userdata = {
#             'user_id': request.session['id'],
#             'username': request.session['username'],
#             'language': request.session['language'],
#             'urls': request.session['urls'],
#         }
#         context = dict()
#         context['data'] = userdata
#         form = OrderForm()
#         context['form'] = form
#         if request.method == 'POST':
#             item_obj = get_object_or_404(Product, pk=int(request.POST['product']))
#             if int(item_obj.quantity_left) < int(request.POST['quantity']):
#                 messages.error(request, 'Product Quantity Exceed')
#                 return redirect('items:OrderListView')
#             smonth, sday, syear = request.POST['ordered_date'].split('/')
#             ordered_date = str(syear) + "-" + str(smonth) + "-" + str(sday)
#             Order.objects.create(product_id=int(request.POST['product']),
#                                  customer_id=int(request.POST['customer']),
#                                  quantity=int(request.POST['quantity']),
#                                  ref_code=request.POST['ref_code'],
#                                  ordered_date=ordered_date,
#                                  shipping_address=request.POST['shipping_address'],
#                                  billing_address=request.POST['billing_address'],
#                                  discount_id=int(request.POST['discount']),
#                                  created_by=int(request.session['id']))
#             Product.objects.filter(id=request.POST['product']).update(
#                 quantity_left=int(item_obj.quantity_left) - int(request.POST['quantity']))
#             o_item = Order.objects.latest('id')
#             Order.objects.filter(id=o_item.id).update(net_total=o_item.get_total())
#             # mail_confirm_notification(self.request, Customer.objects.get(id=self.request.POST['customer']))
#             messages.success(request, 'Data Successfully Saved')
#             return redirect('items:OrderListView')
#         return render(request, 'items/order_form.html', context)
#     except Exception as ex:
#         messages.error(request, str(ex))
#         return redirect('items:OrderListView')


# @method_decorator(login_required("logged_in", 'account:login'), name='dispatch')
# @method_decorator(access_permission_required, name='dispatch')
# class OrderUpdateView(UpdateView):
#     model = Order
#     form_class = OrderForm
#     template_name = 'configuration/order_form.html'
#     success_url = reverse_lazy('configuration:OrderListView')
#
#     def get_context_data(self, **kwargs):
#         userdata = {
#             'user_id': self.request.session['id'],
#             'username': self.request.session['username'],
#             'urls': self.request.session['urls'],
#         }
#         context = super(OrderUpdateView, self).get_context_data(**kwargs)
#         context['data'] = userdata
#         return context
#
#     def form_valid(self, form):
#         if form.is_valid:
#             item = form.save(commit=False)
#             item.net_total = item.get_total()
#             item.updated_date = datetime.today()
#             item.updated_by = self.request.session['id']
#             item.save()
#             messages.success(self.request, 'Data Successfully Updated')
#             return super(OrderUpdateView, self).form_valid(form)
#         else:
#             messages.error(self.request, 'invalid')
#             return super(OrderUpdateView, self).form_invalid(form)


# @login_required("logged_in", 'account:login')
# @access_permission_required
# def OrderDeleteView(request, id):
#     Order.objects.get(pk=id).delete()
#     messages.error(request, 'Data Successfully Deleted')
#     return redirect('items:OrderListView')


def is_connected():
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False


# def mail_confirm_notification(request, cust_obj):
#     mailbody = "Dear " + cust_obj.name + "," + '\n' + '\n' \
#                + "An order has been created successfully. " + '\n' + '\n'
#     mailbody = mailbody + '\n' + "Thanks." + '\n' + "SSMS Team."
#     if is_connected():
#         send_task_mail.delay(mailbody, cust_obj.email)
#         if request.session['language'] == "Eng":
#             messages.success(request, 'A success email has been sent')
#         else:
#             messages.success(request, 'ইমেইল প্রেরণ করা হয়েছে ')
#     else:
#         if request.session['language'] == "Eng":
#             messages.error(request, 'Network Error. Check your internet connection.')
#         else:
#             messages.error(request, 'নেটওয়ার্ক ইরর')
#     return


@csrf_exempt
def check_img(request, product_id):
    img_code = Product.objects.get(id=product_id).image
    img_code = img_code.decode('utf-8')
    response = dict(code=img_code)
    return JsonResponse(response, safe=False)
