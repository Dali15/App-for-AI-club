from django.shortcuts import redirect
from django.http import HttpResponseForbidden

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.role == 'admin' or request.user.role == 'owner'):
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You are not allowed to access this page.")
    return wrapper

def roles_required(allowed_roles):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            # Owner has access to everything
            if request.user.is_authenticated and (request.user.role == 'owner' or request.user.role in allowed_roles):
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("Access denied.")
        return wrapper
    return decorator
