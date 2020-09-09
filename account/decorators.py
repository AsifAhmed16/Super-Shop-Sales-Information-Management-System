from django.shortcuts import render
from functools import wraps
from .models import Users
from permission.models import URL, Privilege
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import resolve


def access_permission_required(view_func):
    def _decorator(request, *args, **kwargs):
        user = request.session['id']
        myfunc, myargs, mykwargs = resolve(request.get_full_path())
        view_function = myfunc.__name__
        userobj = Users.objects.get(id=user)
        index = request.resolver_match.view_name.rindex(':')
        myurl = request.resolver_match.view_name[index+1:]
        try:
            if request.session['id'] == None:
                return render(request, 'account/login.html')
        except:
            return redirect('account:login')
        try:
            urlid = URL.objects.get(url=myurl).id
        except Exception as e:
            print(str(e))
            return render(request, 'includes/404.html')
        access = Privilege.objects.filter(user_id=user, url_id=urlid)
        groupAccess = Privilege.objects.filter(role=userobj.role.id, url_id=urlid)
        if not access.exists() and not groupAccess.exists():
            return render(request, 'includes/404.html')
        response = view_func(request, *args, **kwargs)
        return response
    return wraps(view_func)(_decorator)


def login_required(session_key, fail_redirect_to):
    def _session_required(view_func):
        @wraps(view_func)
        def __session_required(request, *args, **kwargs):
            try:
                session = request.session.get(session_key)
                if session is None:
                    raise ValueError('Login Session is Expired Please Login Again!')
            except KeyError as e:
                messages.error(request, 'Login Session is Expired Please Login Again!')
                return redirect(fail_redirect_to)
            except ValueError as e:
                messages.error(request, 'Login Session is Expired Please Login Again!')
                return redirect(fail_redirect_to)
            else:
                return view_func(request, *args, **kwargs)
        return __session_required
    return _session_required


# def session_required(session_key, fail_redirect_to):
#     def _session_required(view_func):
#         @wraps(view_func)
#         def __session_required(request, *args, **kwargs):
#             current_url = resolve(request.path_info).url_name
#             request.session['redirect_to'] = 'epub:'+ current_url
#             try:
#                 session = request.session.get(session_key)
#                 if session is None:
#                     raise ValueError('Login Session is Expired Please Login Again!')
#             except KeyError as e:
#                 messages.error(request, 'You Are Not Logged In!')
#                 return redirect(fail_redirect_to)
#             except ValueError as e:
#                 messages.error(request, e.message)
#                 return redirect(fail_redirect_to)
#             else:
#                 return view_func(request, *args, **kwargs)
#         return __session_required
#     return _session_required
