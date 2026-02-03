from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ActivityLog(models.Model):
    """Track all user activities and modifications"""
    
    ACTION_CHOICES = [
        ('create', '✨ Créé'),
        ('update', '✏️ Modifié'),
        ('delete', '🗑️ Supprimé'),
        ('view', '👁️ Consulté'),
        ('login', '🔓 Connexion'),
        ('logout', '🔒 Déconnexion'),
        ('register', '📝 Inscription'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='activities')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    content_type = models.CharField(max_length=100, help_text="Type d'objet modifié (Event, User, etc.)")
    object_id = models.IntegerField(null=True, blank=True)
    object_name = models.CharField(max_length=255, help_text="Nom de l'objet modifié")
    old_value = models.TextField(blank=True, help_text="Ancienne valeur")
    new_value = models.TextField(blank=True, help_text="Nouvelle valeur")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, help_text="Navigateur/Device")
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['content_type', '-timestamp']),
            models.Index(fields=['-timestamp']),
        ]
        verbose_name = "Historique d'activité"
        verbose_name_plural = "Historiques d'activités"
    
    def __str__(self):
        return f"{self.user} - {self.get_action_display()} - {self.object_name}"
    
    @property
    def time_ago(self):
        """Return human-readable time ago"""
        from django.utils.timezone import now
        diff = now() - self.timestamp
        
        if diff.days > 0:
            return f"Il y a {diff.days}j"
        elif diff.seconds > 3600:
            return f"Il y a {diff.seconds // 3600}h"
        elif diff.seconds > 60:
            return f"Il y a {diff.seconds // 60}m"
        else:
            return "À l'instant"
