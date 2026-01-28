from django.contrib import admin
from django.utils.html import format_html
from .models import ActivityLog


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('colored_action', 'user_name', 'object_name', 'content_type', 'timestamp_display')
    list_filter = ('action', 'content_type', 'timestamp', 'user')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'object_name')
    readonly_fields = ('user', 'action', 'content_type', 'object_id', 'object_name', 'old_value', 'new_value', 'ip_address', 'user_agent', 'timestamp')
    ordering = ['-timestamp']
    
    fieldsets = (
        ('Informations d\'action', {
            'fields': ('action', 'timestamp', 'user')
        }),
        ('Objet modifié', {
            'fields': ('content_type', 'object_id', 'object_name')
        }),
        ('Détails de modification', {
            'fields': ('old_value', 'new_value'),
            'classes': ('collapse',)
        }),
        ('Informations technique', {
            'fields': ('ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
    )
    
    def colored_action(self, obj):
        colors = {
            'create': '#28a745',    # green
            'update': '#ffc107',    # yellow
            'delete': '#dc3545',    # red
            'view': '#17a2b8',      # cyan
            'login': '#007bff',     # blue
            'logout': '#6c757d',    # gray
            'register': '#20c997',  # teal
        }
        color = colors.get(obj.action, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_action_display()
        )
    colored_action.short_description = 'Action'
    
    def user_name(self, obj):
        if obj.user:
            return f"{obj.user.get_full_name() or obj.user.username}"
        return "Anonyme"
    user_name.short_description = 'Utilisateur'
    
    def timestamp_display(self, obj):
        return obj.timestamp.strftime('%d/%m/%Y %H:%M:%S')
    timestamp_display.short_description = 'Date/Heure'
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
