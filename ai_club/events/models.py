from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Event(models.Model):
    EVENT_TYPE_CHOICES = [
        ('workshop', 'Workshop'),
        ('seminar', 'Seminar'),
        ('meetup', 'Meetup'),
        ('competition', 'Competition'),
        ('social', 'Social Event'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES, default='workshop')
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    max_attendees = models.IntegerField(null=True, blank=True)
    
    # Workshop/Setup Instructions
    setup_instructions = models.TextField(blank=True, help_text="Installation steps, library requirements, setup code, etc.")
    resources_url = models.URLField(max_length=500, blank=True, help_text="GitHub repo, Google Drive, or resource link")
    difficulty_level = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ], default='beginner', blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-date']


class EventRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_registrations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    attended = models.BooleanField(default=False)
    registered_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        unique_together = ('user', 'event')
        ordering = ['-registered_at']

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"
