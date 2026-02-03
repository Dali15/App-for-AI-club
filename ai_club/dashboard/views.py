from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from members.models import Member
from events.models import Event, EventRegistration
from dashboard.models import ActivityLog
from dashboard.role_permissions import ROLE_PERMISSIONS, ALL_AVAILABLE_PERMISSIONS
from accounts.models import User as CustomUser


def home_view(request):
    """Display home page with statistics if user is authenticated."""
    context = {}
    
    if request.user.is_authenticated:
        context.update({
            'total_members': Member.objects.count(),
            'total_events': Event.objects.count(),
            'total_registrations': EventRegistration.objects.count(),
        })
    
    return render(request, 'home.html', context)


@login_required
def dashboard_view(request):
    """Display dashboard with statistics for authorized users."""
    context = {'role': request.user.role}

    # Show statistics for bureau members and admins
    if request.user.is_bureau():
        context.update({
            'total_members': Member.objects.count(),
            'total_events': Event.objects.count(),
            'total_registrations': EventRegistration.objects.count(),
        })

    return render(request, 'dashboard/dashboard.html', context)


@staff_member_required
def activity_history_view(request):
    """Display full activity history - Admin only"""
    query = request.GET.get('q', '')
    action_filter = request.GET.get('action', '')
    user_filter = request.GET.get('user', '')
    content_type_filter = request.GET.get('content_type', '')
    
    logs = ActivityLog.objects.all()
    
    # Search filter
    if query:
        logs = logs.filter(
            Q(object_name__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(user__username__icontains=query)
        )
    
    # Action filter
    if action_filter:
        logs = logs.filter(action=action_filter)
    
    # User filter
    if user_filter:
        logs = logs.filter(user_id=user_filter)
    
    # Content type filter
    if content_type_filter:
        logs = logs.filter(content_type=content_type_filter)
    
    # Pagination
    paginator = Paginator(logs, 50)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Get filter options
    actions = ActivityLog.ACTION_CHOICES
    users = logs.values_list('user', flat=True).distinct()
    content_types = logs.values_list('content_type', flat=True).distinct().order_by('content_type')
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'action_filter': action_filter,
        'user_filter': user_filter,
        'content_type_filter': content_type_filter,
        'actions': actions,
        'users': users,
        'content_types': content_types,
    }
    
    return render(request, 'dashboard/activity_history.html', context)


def is_owner_or_president(user):
    """Check if user is owner (superuser) or president"""
    return user.is_superuser or user.role == 'president'


@login_required
def manage_permissions_view(request):
    """Manage role permissions - Owner and President only"""
    
    # Check permissions
    if not is_owner_or_president(request.user):
        return redirect('dashboard')
    
    # Get all roles with their current permissions
    roles_data = []
    for role_key, role_info in ROLE_PERMISSIONS.items():
        roles_data.append({
            'key': role_key,
            'label': role_info['label'],
            'permissions': role_info['permissions'],
            'available_permissions': ALL_AVAILABLE_PERMISSIONS,
        })
    
    context = {
        'roles_data': roles_data,
        'all_permissions': ALL_AVAILABLE_PERMISSIONS,
        'user_is_admin': request.user.is_superuser,
    }
    
    return render(request, 'dashboard/manage_permissions.html', context)


@login_required
@require_http_methods(["POST"])
def update_role_permission_view(request):
    """Update permission for a specific role - Owner and President only"""
    
    # Check permissions
    if not is_owner_or_president(request.user):
        return JsonResponse({'success': False, 'message': 'Accès refusé'}, status=403)
    
    role = request.POST.get('role')
    permission = request.POST.get('permission')
    action = request.POST.get('action')  # 'add' or 'remove'
    
    if role not in ROLE_PERMISSIONS or not permission:
        return JsonResponse({'success': False, 'message': 'Données invalides'}, status=400)
    
    # Update the permission
    if action == 'add':
        if permission not in ROLE_PERMISSIONS[role]['permissions']:
            ROLE_PERMISSIONS[role]['permissions'].append(permission)
    elif action == 'remove':
        if permission in ROLE_PERMISSIONS[role]['permissions']:
            ROLE_PERMISSIONS[role]['permissions'].remove(permission)
    else:
        return JsonResponse({'success': False, 'message': 'Action invalide'}, status=400)
    
    # Log the change
    ActivityLog.objects.create(
        user=request.user,
        action='update',
        content_type='Permission',
        object_name=f"{role} - {permission}",
        new_value=f"{'Ajoutée' if action == 'add' else 'Supprimée'}: {permission}",
    )
    
    return JsonResponse({
        'success': True,
        'message': f"Permission {'ajoutée' if action == 'add' else 'supprimée'} avec succès",
        'permissions': ROLE_PERMISSIONS[role]['permissions'],
    })


@login_required
def view_role_permissions_view(request, role=None):
    """View permissions for a specific role"""
    
    if not role or role not in ROLE_PERMISSIONS:
        return redirect('manage_permissions')
    
    role_info = ROLE_PERMISSIONS[role]
    available_perms = [perm[0] for perm in ALL_AVAILABLE_PERMISSIONS]
    
    context = {
        'role': role,
        'role_label': role_info['label'],
        'permissions': role_info['permissions'],
        'available_permissions': ALL_AVAILABLE_PERMISSIONS,
        'is_owner_or_president': is_owner_or_president(request.user),
    }
    
    return render(request, 'dashboard/view_role_permissions.html', context)
