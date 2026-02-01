from django.db import models

# Create your models here.
from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('owner', 'Owner'),
        ('president', 'President'),
        ('vice_president', 'Vice President'),
        ('partnerships', 'Responsable Partenariats'),
        ('design', 'Responsable Design'),
        ('treasurer', 'Treasurer'),
        ('secretary', 'Secretaire'), # New Role
        ('hr', 'Responsable RH'),
        ('media', 'Responsable Media'),
        ('events_manager', 'Responsable Événement'),
        ('member', 'Membre actif'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='member',
        verbose_name="Primary Role"
    )
    
    secondary_role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        blank=True,
        null=True,
        verbose_name="Secondary Role (Optional)"
    )
    
    # Member Profile Fields
    bio = models.TextField(blank=True, help_text="About you")
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    skills = models.CharField(max_length=500, blank=True, help_text="e.g., Python, Machine Learning, Deep Learning, NLP")
    github_url = models.URLField(max_length=500, blank=True)
    linkedin_url = models.URLField(max_length=500, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_bureau(self):
        # Bureau if either role is not member, or staff/superuser
        is_primary_bureau = self.role != 'member'
        is_secondary_bureau = self.secondary_role and self.secondary_role != 'member'
        return is_primary_bureau or is_secondary_bureau or self.is_staff or self.is_superuser

    def save(self, *args, **kwargs):
        # Role permission enforcement is now handled by the post_save signal
        super().save(*args, **kwargs)

    def __str__(self):
        if self.secondary_role:
            return f"{self.username} ({self.get_role_display()} & {self.get_secondary_role_display()})"
        return f"{self.username} ({self.get_role_display()})"
    
    class Meta:
        ordering = ['-created_at']

# Signal to sync roles with Django Groups and Permissions
from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

@receiver(post_save, sender=User)
def sync_user_permissions(sender, instance, created, **kwargs):
    """
    Automatically assign strict permissions based on role.
    Run on every save to ensure role changes immediately update access.
    """
    if kwargs.get('raw', False):
        return

    updates = {}
    
    # Check both roles for Owner/President status
    roles = [instance.role]
    if instance.secondary_role:
        roles.append(instance.secondary_role)
        
    is_top_admin = 'owner' in roles or 'president' in roles
    
    if is_top_admin:
        # Ensure they are staff and superuser
        if not instance.is_staff or not instance.is_superuser:
            User.objects.filter(pk=instance.pk).update(is_staff=True, is_superuser=True)
            # Update instance in memory to reflect change (though purely local here)
            instance.is_staff = True
            instance.is_superuser = True
        return

    # For other roles, they might need is_staff=True to access admin, 
    # but we restrict what they can see via Groups.
    
    # Define Role-to-Permission Mapping
    # Format: 'role_name': [('app_label', 'model_name', ['view', 'add', 'change', 'delete'])]
    
    PERMISSIONS_MAP = {
        'treasurer': [
            ('members', 'member', ['view']),  # Treasurer sees members only
        ],
        'secretary': [
            ('members', 'member', ['view', 'change']),  # Secretary manages members
            ('announcements', 'announcement', ['view', 'add', 'change']), # And announcements
            ('events', 'event', ['view']), # Can view events logic
        ],
        'hr': [
            ('members', 'member', ['view', 'change']),  # HR sees and can edit members (e.g. profiles)
        ],
        'events_manager': [
            ('events', 'event', ['view', 'add', 'change', 'delete']),
            ('events', 'eventregistration', ['view', 'add', 'change']),
        ],
        'media': [
            ('announcements', 'announcement', ['view', 'add', 'change']),
        ],
        'partnerships': [
            ('projects', 'project', ['view', 'add', 'change']),
        ],
        'member': [] # Regular members get NOTHING
    }

    # Grant permissions but RESTRICT Admin Panel access (is_staff=False)
    # Only Owner/President can access the Django Admin Panel.
    
    # Combine permissions from both roles
    target_permissions = []
    
    # Add primary role perms
    target_permissions.extend(PERMISSIONS_MAP.get(instance.role, []))
    
    # Add secondary role perms
    if instance.secondary_role:
        target_permissions.extend(PERMISSIONS_MAP.get(instance.secondary_role, []))
    
    # Force is_staff=False and is_superuser=False for all these roles
    
    # Force is_staff=False and is_superuser=False for all these roles
    if instance.is_staff or instance.is_superuser:
        User.objects.filter(pk=instance.pk).update(is_staff=False, is_superuser=False)
        instance.is_staff = False
        instance.is_superuser = False

    # Assign permissions for Frontend access
    # Note: M2M operations do NOT trigger post_save on the User model, so this is safe.
    instance.user_permissions.clear()
    for app, model, actions in target_permissions:
        try:
            content_type = ContentType.objects.get(app_label=app, model=model)
            for action in actions:
                codename = f'{action}_{model}'
                try:
                    perm = Permission.objects.get(content_type=content_type, codename=codename)
                    instance.user_permissions.add(perm)
                except Permission.DoesNotExist:
                    pass
        except ContentType.DoesNotExist:
            continue


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

