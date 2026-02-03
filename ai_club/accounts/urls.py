from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='accounts/login.html'),
        name='login'
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='home'),
        name='logout'
    ),
    path(
        'signup/',
        views.signup_view,
        name='signup'
    ),
    path('pending-members/', views.pending_members, name='pending_members'),
    path('approve-member/<int:user_id>/', views.approve_member, name='approve_member'),
    path('reject-member/<int:user_id>/', views.reject_member, name='reject_member'),
]
