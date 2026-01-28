from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class FAQ(models.Model):
    """Frequently Asked Questions for the assistant"""
    question = models.CharField(max_length=500)
    answer = models.TextField()
    keywords = models.CharField(
        max_length=500, 
        help_text="Comma-separated keywords (e.g., 'event, registration, when')"
    )
    category = models.CharField(
        max_length=100,
        choices=[
            ('events', 'Events'),
            ('registration', 'Registration'),
            ('members', 'Members'),
            ('projects', 'Projects'),
            ('announcements', 'Announcements'),
            ('general', 'General'),
        ],
        default='general'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ['category', 'question']

    def __str__(self):
        return self.question


class ChatMessage(models.Model):
    """Store chat conversations between users and assistant"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages')
    message = models.TextField()  # User's message
    response = models.TextField()  # Assistant's response
    category = models.CharField(max_length=50, blank=True)  # FAQ category used
    is_faq = models.BooleanField(default=False)  # Was it from FAQ?
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.message[:50]}"
