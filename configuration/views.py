from django.urls import reverse_lazy
from account.decorators import *
from .forms import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from datetime import datetime
from django.utils.decorators import method_decorator


@method_decorator(login_required("logged_in", 'account:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class CategoryListView(ListView):
    model = Category
    template_name = 'configuration/category_list.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'language': self.request.session['language'],
            'urls': self.request.session['urls'],
        }
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['data'] = userdata
        return context


@method_decorator(login_required("logged_in", 'account:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'configuration/category_form.html'
    success_url = reverse_lazy('configuration:CategoryListView')

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'language': self.request.session['language'],
            'urls': self.request.session['urls'],
        }
        context = super(CategoryCreateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['form'] = self.form_class
        return context

    def form_valid(self, form):
        if form.is_valid:
            item = form.save(commit=False)
            item.created_date = datetime.today()
            item.created_by = self.request.session['id']
            item.save()
            messages.success(self.request, 'Data Successfully Saved')
            return super(CategoryCreateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(CategoryCreateView, self).form_invalid(form)


@method_decorator(login_required("logged_in", 'account:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'configuration/category_form.html'
    success_url = reverse_lazy('configuration:CategoryListView')

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'language': self.request.session['language'],
            'urls': self.request.session['urls'],
        }
        context = super(CategoryUpdateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        return context

    def form_valid(self, form):
        if form.is_valid:
            item = form.save(commit=False)
            item.updated_date = datetime.today()
            item.updated_by = self.request.session['id']
            item.save()
            messages.success(self.request, 'Data Successfully Updated')
            return super(CategoryUpdateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(CategoryUpdateView, self).form_invalid(form)


@login_required("logged_in", 'account:login')
@access_permission_required
def CategoryDeleteView(request, id):
    Category.objects.get(pk=id).delete()
    messages.error(request, 'Data Successfully Deleted')
    return redirect('configuration:CategoryListView')


@method_decorator(login_required("logged_in", 'account:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class DiscountListView(ListView):
    model = Discount
    template_name = 'configuration/discount_list.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'language': self.request.session['language'],
            'urls': self.request.session['urls'],
        }
        context = super(DiscountListView, self).get_context_data(**kwargs)
        context['data'] = userdata
        return context


@method_decorator(login_required("logged_in", 'account:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class DiscountCreateView(CreateView):
    model = Discount
    form_class = DiscountForm
    template_name = 'configuration/discount_form.html'
    success_url = reverse_lazy('configuration:DiscountListView')

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'language': self.request.session['language'],
            'urls': self.request.session['urls'],
        }
        context = super(DiscountCreateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        context['form'] = self.form_class
        return context

    def form_valid(self, form):
        if form.is_valid:
            item = form.save(commit=False)
            item.created_date = datetime.today()
            item.created_by = self.request.session['id']
            item.save()
            messages.success(self.request, 'Data Successfully Saved')
            return super(DiscountCreateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(DiscountCreateView, self).form_invalid(form)


@method_decorator(login_required("logged_in", 'account:login'), name='dispatch')
@method_decorator(access_permission_required, name='dispatch')
class DiscountUpdateView(UpdateView):
    model = Discount
    form_class = DiscountForm
    template_name = 'configuration/discount_form.html'
    success_url = reverse_lazy('configuration:DiscountListView')

    def get_context_data(self, **kwargs):
        userdata = {
            'user_id': self.request.session['id'],
            'username': self.request.session['username'],
            'language': self.request.session['language'],
            'urls': self.request.session['urls'],
        }
        context = super(DiscountUpdateView, self).get_context_data(**kwargs)
        context['data'] = userdata
        return context

    def form_valid(self, form):
        if form.is_valid:
            item = form.save(commit=False)
            item.updated_date = datetime.today()
            item.updated_by = self.request.session['id']
            item.save()
            messages.success(self.request, 'Data Successfully Updated')
            return super(DiscountUpdateView, self).form_valid(form)
        else:
            messages.error(self.request, 'invalid')
            return super(DiscountUpdateView, self).form_invalid(form)


@login_required("logged_in", 'account:login')
@access_permission_required
def DiscountDeleteView(request, id):
    Discount.objects.get(pk=id).delete()
    messages.error(request, 'Data Successfully Deleted')
    return redirect('configuration:DiscountListView')
