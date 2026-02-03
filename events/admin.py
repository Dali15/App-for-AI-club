from django.contrib import admin
from .models import Event, EventRegistration


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Event Management with Workshop Features."""
    
    list_display = ('title', 'event_type', 'difficulty_level', 'date', 'location', 'registration_count', 'created_by')
    list_filter = ('event_type', 'difficulty_level', 'date', 'created_by')
    search_fields = ('title', 'description', 'location')
    readonly_fields = ('created_by', 'created_at', 'updated_at', 'registration_count')
    
    fieldsets = (
        ('Event Details', {
            'fields': ('title', 'description', 'event_type', 'date', 'location', 'max_attendees')
        }),
        ('Workshop Information', {
            'fields': ('difficulty_level', 'setup_instructions', 'resources_url'),
            'classes': ('collapse',)
        }),
        ('Organizer', {'fields': ('created_by',)}),
        ('Metadata', {'fields': ('created_at', 'updated_at', 'registration_count')}),
    )
    
    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields
    
    def registration_count(self, obj):
        return obj.registrations.count()
    registration_count.short_description = 'Total Registrations'


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    """Event Registration Management."""
    
    list_display = ('user', 'event', 'attended', 'registered_at')
    list_filter = ('event', 'attended', 'registered_at')
    search_fields = ('user__username', 'event__title')
    readonly_fields = ('registered_at',)
    
    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields
