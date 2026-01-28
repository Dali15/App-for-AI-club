from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages

def open_admin_login(request):
    """
    Allow any user to access admin panel temporarily
    """
    if not request.user.is_authenticated:
        messages.error(request, 'Please login first')
        return redirect('login')
    
    # Allow any authenticated user to access admin
    return redirect('admin')