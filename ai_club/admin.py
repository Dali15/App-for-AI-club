from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect

User = get_user_model()

# Override admin site to allow any authenticated user
class OpenAdminSite(admin.AdminSite):
    def has_permission(self, request):
        """
        Allow any authenticated user to access admin
        """
        return request.user.is_authenticated

# Create custom admin site
admin_site = OpenAdminSite(name='admin_site')

# Register User model with custom admin
@admin_site.register(User)
class CustomUserAdmin(UserAdmin):
    pass

# Override the admin login view
def admin_login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(request.path_info)
    return admin_site.login(request)

# Override the admin logout view  
def admin_logout_view(request):
    return admin_site.logout(request)