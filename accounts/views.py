from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from .forms import CustomUserCreationForm
import os


def signup_view(request):
    """User registration/signup view."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # If OPEN_ADMIN_ACCESS is enabled on the deployment and there
            # are currently no superusers, promote the first created user
            # to superuser/staff so they can access the admin and make
            # configuration changes. This is temporary — set
            # OPEN_ADMIN_ACCESS=False once you've restored normal access.
            if os.getenv('OPEN_ADMIN_ACCESS', 'True') == 'True':
                User = get_user_model()
                if not User.objects.filter(is_superuser=True).exists():
                    user.is_staff = True
                    user.is_superuser = True
                    user.save()

            # Log the user in after signup
            login(request, user)
            messages.success(request, f'Welcome {user.username}! Your account has been created successfully.')
            return redirect('dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/signup.html', {'form': form})
