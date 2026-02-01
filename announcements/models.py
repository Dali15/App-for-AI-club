from django.conf import settings

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    # Author is optional for existing records, but we should make it required for new ones.
    # We'll set null=True for migration compatibility then enforce logic in views.
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    is_approved = models.BooleanField(default=False, help_text="Approved by President/Owner")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
