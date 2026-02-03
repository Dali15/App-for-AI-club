from django.contrib import admin
from .models import Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    """Member Management in Admin."""
    
    list_display = ('username', 'email', 'role', 'join_date', 'is_active')
    list_filter = ('join_date', 'user__role')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('join_date',)
    date_hierarchy = 'join_date'
    
    def username(self, obj):
        return obj.user.username
    username.short_description = 'Username'
    
    def email(self, obj):
        return obj.user.email
    email.short_description = 'Email'
    
    def role(self, obj):
        return obj.user.get_role_display()
    role.short_description = 'Role'
    
    def is_active(self, obj):
        return obj.user.is_active
    is_active.boolean = True
    is_active.short_description = 'Active'
