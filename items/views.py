from .forms import *
from django.urls import reverse_lazy
from account.decorators import *
from django.views.generic import ListView, CreateView, UpdateView
from datetime import datetime
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404


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
            'urls': self.request.session['urls'],
        }
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['form'] = self.form_class
        return context

    def form_valid(self, form):
        if form.is_valid:
            item = form.save(commit=False)
            item.image = self.request.POST['b64']
            item.created_date = datetime.today()
            item.created_by = self.request.session['id']
            item.save()
            messages.success(self.request, 'Data Successfully Saved')
            return super(ProductCreateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(ProductCreateView, self).form_invalid(form)


@login_required("logged_in", 'account:login')
@access_permission_required
def ProductUpdateView(request, id):
    try:
        userdata = {
            'user_id': request.session['id'],
            'username': request.session['username'],
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
            item.save()
            messages.success(self.request, 'Data Successfully Saved')
            return super(StockCreateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(StockCreateView, self).form_invalid(form)


@login_required("logged_in", 'account:login')
@access_permission_required
def StockUpdateView(request, id):
    try:
        userdata = {
            'user_id': request.session['id'],
            'username': request.session['username'],
            'urls': request.session['urls'],
        }
        item_obj = get_object_or_404(Stock, pk=id)
        form = StockForm(request.POST or None, instance=item_obj)
        context = dict()
        context['data'] = userdata
        context['form'] = form
        if request.method == 'POST' and id:
            if form.is_valid():
                item = form.save(commit=False)
                item.total_price = item.get_total()
                item.updated_by = request.session['id']
                item.updated_date = datetime.now()
                item.save()
                messages.success(request, 'Data Successfully Updated')
                return redirect('items:StockListView')
        return render(request, 'items/stock_form.html', context)
    except Exception as ex:
        messages.error(request, str(ex))
        return redirect('items:StockListView')


@login_required("logged_in", 'account:login')
@access_permission_required
def StockDeleteView(request, id):
    Stock.objects.get(pk=id).delete()
    messages.error(request, 'Data Successfully Deleted')
    return redirect('items:StockListView')


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
            'urls': self.request.session['urls'],
        }
        context = super(OrderListView, self).get_context_data(**kwargs)
        context['data'] = userdata
        return context


@method_decorator(login_required("logged_in", 'account:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'items/order_form.html'
    success_url = reverse_lazy('items:OrderListView')

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(OrderCreateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['form'] = self.form_class
        return context

    def form_valid(self, form):
        if form.is_valid:
            item = form.save(commit=False)
            item.net_total = item.get_total()
            item.created_date = datetime.today()
            item.created_by = self.request.session['id']
            item.save()
            messages.success(self.request, 'Data Successfully Saved')
            return super(OrderCreateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(OrderCreateView, self).form_invalid(form)


@method_decorator(login_required("logged_in", 'account:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'configuration/order_form.html'
    success_url = reverse_lazy('configuration:OrderListView')

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'urls': self.request.session['urls'],
        }
        context = super(OrderUpdateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        return context

    def form_valid(self, form):
        if form.is_valid:
            item = form.save(commit=False)
            item.net_total = item.get_total()
            item.updated_date = datetime.today()
            item.updated_by = self.request.session['id']
            item.save()
            messages.success(self.request, 'Data Successfully Updated')
            return super(OrderUpdateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(OrderUpdateView, self).form_invalid(form)


@login_required("logged_in", 'account:login')
@access_permission_required
def OrderDeleteView(request, id):
    Order.objects.get(pk=id).delete()
    messages.error(request, 'Data Successfully Deleted')
    return redirect('items:OrderListView')
