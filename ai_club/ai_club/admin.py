from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

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