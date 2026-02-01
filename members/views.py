from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from accounts.models import User
from events.models import EventRegistration
from dashboard.permissions import require_permission


@require_permission('view_members')
def member_list(request):
    """Display all club members with search - requires view_members permission."""
    members = User.objects.filter(is_active=True).exclude(role='president')
    
    search_query = request.GET.get('search', '')
    if search_query:
        members = members.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(skills__icontains=search_query)
        )
    
    # Get attendance stats
    for member in members:
        member.events_attended = EventRegistration.objects.filter(
            user=member, 
            attended=True
        ).count()
    
    context = {
        'members': members,
        'search_query': search_query,
        'total_members': User.objects.filter(is_active=True).count(),
    }
    return render(request, 'members/member_list.html', context)


@login_required
def member_profile(request, user_id):
    """Display member profile with skills, projects, and attendance."""
    member = get_object_or_404(User, id=user_id, is_active=True)
    
    # Get attendance info
    attended_events = EventRegistration.objects.filter(
        user=member, 
        attended=True
    ).select_related('event').order_by('-event__date')
    
    registered_events = EventRegistration.objects.filter(
        user=member,
        attended=False
    ).select_related('event').order_by('event__date')
    
    context = {
        'member': member,
        'attended_events': attended_events,
        'registered_events': registered_events,
        'total_attended': attended_events.count(),
        'can_manage_roles': request.user.has_perm('accounts.change_user'),
        'role_choices': User.ROLE_CHOICES,
    }
    return render(request, 'members/member_profile.html', context)

@login_required
def manage_user_role(request, user_id):
    """Update user role - requires change_user permission."""
    if not request.user.has_perm('accounts.change_user'):
        messages.error(request, "Permission denied.")
        return redirect('dashboard')
        
    if request.method == 'POST':
        target_user = get_object_or_404(User, id=user_id)
        new_role = request.POST.get('role')
        new_secondary_role = request.POST.get('secondary_role')
        
        # Prevent editing Owner if you are not Owner
        if target_user.role == 'owner' and request.user.role != 'owner':
             messages.error(request, "Only the Owner can modify the Owner's role.")
             return redirect('member_profile', user_id=user_id)
        
        if new_role:
            target_user.role = new_role
        
        # secondary_role can be empty
        target_user.secondary_role = new_secondary_role if new_secondary_role else ''
        
        target_user.save() # Signal triggers permission update
        messages.success(request, f"Role for {target_user.username} updated to {target_user.get_role_display()}")
        
    return redirect('member_profile', user_id=user_id)


@login_required
def edit_profile(request):
    """Allow user to edit their own profile."""
    if request.method == 'POST':
        user = request.user
        user.bio = request.POST.get('bio', user.bio)
        user.skills = request.POST.get('skills', user.skills)
        user.github_url = request.POST.get('github_url', user.github_url)
        user.linkedin_url = request.POST.get('linkedin_url', user.linkedin_url)
        user.phone = request.POST.get('phone', user.phone)
        
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
        
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('member_profile', user_id=user.id)
    
    context = {'member': request.user}
    return render(request, 'members/edit_profile.html', context)
