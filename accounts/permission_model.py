from django.db import models
from accounts.models import User


class RolePermission(models.Model):
    """Define permissions for each role across all features"""
    
    ROLE_CHOICES = User.ROLE_CHOICES
    
    FEATURE_CHOICES = (
        ('create_event', 'Create Events'),
        ('edit_event', 'Edit Events'),
        ('delete_event', 'Delete Events'),
        ('create_announcement', 'Create Announcements'),
        ('edit_announcement', 'Edit Announcements'),
        ('delete_announcement', 'Delete Announcements'),
        ('create_project', 'Create Projects'),
        ('edit_project', 'Edit Projects'),
        ('delete_project', 'Delete Projects'),
        ('add_project_file', 'Add Files to Projects'),
        ('delete_project_file', 'Delete Project Files'),
        ('post_project_update', 'Post Project Updates'),
        ('access_admin', 'Access Admin Panel'),
        ('manage_users', 'Manage Users'),
        ('manage_roles', 'Manage User Roles'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    feature = models.CharField(max_length=50, choices=FEATURE_CHOICES)
    can_perform = models.BooleanField(default=False, help_text="Check to allow this role to perform this action")
    description = models.TextField(blank=True, help_text="Explanation of what this permission allows")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('role', 'feature')
        verbose_name_plural = 'Role Permissions'
        ordering = ['role', 'feature']
    
    def __str__(self):
        return f"{self.get_role_display()} - {self.get_feature_display()}"
    
    @classmethod
    def has_permission(cls, role, feature):
        """Check if a role has permission for a feature"""
        # Owner always has all permissions
        if role == 'owner':
            return True
        
        try:
            permission = cls.objects.get(role=role, feature=feature)
            return permission.can_perform
        except cls.DoesNotExist:
            return False
    
    @classmethod
    def initialize_defaults(cls):
        """Initialize default permissions for all roles"""
        defaults = {
            'owner': [
                'create_event', 'edit_event', 'delete_event',
                'create_announcement', 'edit_announcement', 'delete_announcement',
                'create_project', 'edit_project', 'delete_project',
                'add_project_file', 'delete_project_file', 'post_project_update',
                'access_admin', 'manage_users', 'manage_roles'
            ],
            'president': [
                'create_event', 'edit_event', 'delete_event',
                'create_announcement', 'edit_announcement', 'delete_announcement',
                'create_project', 'edit_project', 'delete_project',
                'add_project_file', 'delete_project_file', 'post_project_update',
                'access_admin'
            ],
            'vice_president': [
                'create_event', 'edit_event', 'delete_event',
                'create_announcement', 'edit_announcement', 'delete_announcement',
                'create_project', 'edit_project', 'delete_project',
                'add_project_file', 'delete_project_file', 'post_project_update',
                'access_admin'
            ],
            'events_manager': [
                'create_event', 'edit_event', 'delete_event',
                'create_project', 'add_project_file', 'post_project_update'
            ],
            'media': [
                'create_announcement', 'edit_announcement', 'delete_announcement',
                'create_project', 'add_project_file', 'post_project_update'
            ],
            'hr': [
                'create_announcement', 'edit_announcement',
                'create_project', 'add_project_file', 'post_project_update'
            ],
            'partnerships': [
                'create_announcement',
                'create_project', 'add_project_file', 'post_project_update'
            ],
            'design': [
                'create_project', 'add_project_file', 'post_project_update'
            ],
            'treasurer': [],
            'member': []
        }
        
        for role, features in defaults.items():
            for feature, _ in cls.FEATURE_CHOICES:
                obj, created = cls.objects.get_or_create(
                    role=role,
                    feature=feature,
                    defaults={'can_perform': feature in features}
                )
