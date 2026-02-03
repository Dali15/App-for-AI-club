from django.shortcuts import redirect
from django.contrib import messages
from dashboard.role_permissions import ROLE_PERMISSIONS


def has_permission(user, permission):
    """Check if user has permission using Django's built-in system."""
    if user.is_superuser:
        return True
        
    # Map legacy functional permissions to Django model permissions
    PERMISSION_MAPPING = {
        'view_members': 'accounts.view_user',
        'manage_members': 'accounts.change_user',
        'create_event': 'events.add_event',
        'edit_event': 'events.change_event',
        'delete_event': 'events.delete_event',
        'view_events': 'events.view_event',
        'create_announcement': 'announcements.add_announcement',
        'edit_announcement': 'announcements.change_announcement',
        'delete_announcement': 'announcements.delete_announcement',
        'create_project': 'projects.add_project',
        'edit_project': 'projects.change_project',
        # Add more mappings as needed
    }
    
    django_perm = PERMISSION_MAPPING.get(permission)
    if django_perm:
        return user.has_perm(django_perm)
    
    # Fallback to old Role check if not mapped (or return False)
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
