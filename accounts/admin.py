from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, RolePermission
import os

# Allow temporarily opening the admin site to any authenticated user.
# Control via the environment variable `OPEN_ADMIN_ACCESS`.
OPEN_ADMIN_ACCESS = os.getenv('OPEN_ADMIN_ACCESS', 'True') == 'True'


class OpenAdminSite(admin.AdminSite):
    """Admin site that grants access to any authenticated user."""

    def has_permission(self, request):
        return request.user.is_authenticated


if OPEN_ADMIN_ACCESS:
    admin.site = OpenAdminSite(name='admin_site')


# Customize admin site
admin.site.site_header = "🎓 AI Club Admin Panel"
admin.site.site_title = "AI Club Admin"
admin.site.index_title = "Welcome to AI Club Management"


class CustomUserAdmin(UserAdmin):
    """Custom User Admin with role management and member profile."""
    
    fieldsets = UserAdmin.fieldsets + (
        ('Club Information', {'fields': ('role',)}),
        ('Member Profile', {
            'fields': ('bio', 'profile_picture', 'skills', 'github_url', 'linkedin_url', 'phone'),
            'classes': ('collapse',)
        }),
    )
    
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'skills', 'is_active')
    list_filter = ('role', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'skills')
    ordering = ('-date_joined',)
    
    def get_readonly_fields(self, request, obj=None):
        readonly = list(super().get_readonly_fields(request, obj))
        if not request.user.is_superuser:
            readonly.append('date_joined')
        return readonly


admin.site.register(User, CustomUserAdmin)


class RolePermissionAdmin(admin.ModelAdmin):
    """Admin interface for managing role permissions"""
    
    list_display = ('role', 'feature', 'can_perform', 'description_short')
    list_filter = ('role', 'feature', 'can_perform')
    search_fields = ('role', 'feature', 'description')
    
    fieldsets = (
        ('Role & Feature', {
            'fields': ('role', 'feature'),
            'description': 'Select the role and feature combination'
        }),
        ('Permission Settings', {
            'fields': ('can_perform', 'description'),
        }),
    )
    
    list_editable = ('can_perform',)  # Allow inline editing
    
    def description_short(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    description_short.short_description = 'Description'
    
    def get_readonly_fields(self, request, obj=None):
        # Role and feature should not be editable after creation
        if obj is not None:
            return self.readonly_fields + ('role', 'feature')
        return self.readonly_fields
    
    def changelist_view(self, request, extra_context=None):
        """Add helpful info to the changelist view"""
        extra_context = extra_context or {}
        extra_context['title'] = 'Manage Role Permissions'
        return super().changelist_view(request, extra_context=extra_context)


# Hide RolePermission from admin (use matrix instead)
# admin.site.register(RolePermission, RolePermissionAdmin)

