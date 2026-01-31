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
        ('hr', 'Responsable RH'),
        ('media', 'Responsable Media'),
        ('events_manager', 'Responsable Événement'),
        ('member', 'Membre actif'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='member'
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
        return self.role != 'member' or self.is_staff or self.is_superuser

    def save(self, *args, **kwargs):
        # Automatically make bureau members staff/superuser so they can access admin
        if self.role in ['owner', 'president', 'vice_president']:
            self.is_staff = True
            self.is_superuser = True
        elif self.role != 'member':
             # Other bureau members get staff access but maybe not superuser (can be refined)
             self.is_staff = True
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.role})"
    
    class Meta:
        ordering = ['-created_at']


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

