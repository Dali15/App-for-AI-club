from django.shortcuts import redirect
from django.contrib import messages
from dashboard.role_permissions import ROLE_PERMISSIONS


def has_permission(user, permission):
    """Check if user has permission"""
    if user.is_superuser:
        return True
    role = getattr(user, 'role', 'member')
    if role in ROLE_PERMISSIONS:
        return permission in ROLE_PERMISSIONS[role]['permissions']
    return False


def require_permission(permission):
    """Decorator to require a specific permission"""
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not has_permission(request.user, permission):
                messages.error(request, f"Vous n'avez pas la permission: {permission}")
                return redirect('dashboard')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
