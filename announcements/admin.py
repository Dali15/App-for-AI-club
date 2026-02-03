from django.contrib import admin
from .models import Announcement


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    """Announcement Management in Admin."""
    
    list_display = ('title', 'created_at', 'preview')
    list_filter = ('created_at',)
    search_fields = ('title', 'content')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Announcement', {'fields': ('title', 'content')}),
        ('Metadata', {'fields': ('created_at',), 'classes': ('collapse',)}),
    )
    
    def preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    preview.short_description = 'Content Preview'
