from django.contrib import admin
from .models import FAQ, ChatMessage


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('question', 'answer', 'keywords')
    fieldsets = (
        ('Question & Answer', {
            'fields': ('question', 'answer')
        }),
        ('Settings', {
            'fields': ('keywords', 'category', 'is_active')
        }),
    )


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'message_preview', 'category', 'is_faq', 'created_at')
    list_filter = ('category', 'is_faq', 'created_at', 'user')
    search_fields = ('message', 'response', 'user__username')
    readonly_fields = ('user', 'message', 'response', 'category', 'is_faq', 'created_at')
    
    def message_preview(self, obj):
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message
    message_preview.short_description = "Message"
    
    def has_add_permission(self, request):
        return False
