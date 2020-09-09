from datetime import datetime, timedelta
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from account.models import Role
from account.forms import RolesForm


# Role Module
def product_list(request):
    try:
        language = "Eng"
        if 'language' in request.session:
            language = request.session['language']
        userdata = {
            'user_id': request.session['id'],
            'username': request.session['username'],
            'language': language,
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


def product_process(request, id=None):
    try:
        form = RolesForm
        userdata = {
            'user_id': request.session['id'],
            'username': request.session['username'],
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
                editform.updated_date = (datetime.now() + timedelta(hours=6))
                editform.save()
                messages.success(request, 'Data Updated')
                return redirect('account:product_list')
        elif id:
            roleobj = get_object_or_404(Role, pk=id)
            form = RolesForm(request.POST or None, instance=roleobj)
            context['form'] = form
        elif request.method == 'POST':
            form = RolesForm(request.POST, request.FILES or None)
            if form.is_valid():
                process_area = form.save(commit=False)
                process_area.created_date = (datetime.now() + timedelta(hours=6))
                process_area.created_by = request.session['id']
                process_area.save()
                messages.success(request, 'Data Successfully Saved')
                return redirect('account:product_list')
            else:
                context = {
                    'data': userdata,
                    'form': form
                }
                return render(request, 'account/roles_form.html', context)
        return render(request, 'account/roles_form.html', context)
    except Exception as ex:
        messages.error(request, str(ex))
        return redirect('account:product_list')


def product_delete(request, id):
    Role.objects.get(pk=id).delete()
    messages.error(request, 'Data Deleted')
    return redirect('account:product_list')
