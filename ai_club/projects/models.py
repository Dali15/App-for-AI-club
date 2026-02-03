from django.db import models
from accounts.models import User


class Project(models.Model):
    """Project model for team collaboration"""
    
    CATEGORY_CHOICES = (
        ('web', 'Web Development'),
        ('ai', 'AI/Machine Learning'),
        ('mobile', 'Mobile App'),
        ('data', 'Data Science'),
        ('game', 'Game Development'),
        ('other', 'Other'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Project metadata
    repository_url = models.URLField(blank=True, null=True, help_text="GitHub or other repo link")
    documentation_url = models.URLField(blank=True, null=True, help_text="Link to documentation")
    status = models.CharField(
        max_length=20,
        choices=(
            ('planning', 'Planning'),
            ('active', 'Active Development'),
            ('completed', 'Completed'),
            ('archived', 'Archived'),
        ),
        default='active'
    )
    
    # Team members
    members = models.ManyToManyField(User, related_name='projects', blank=True)
    
    # Visibility
    is_public = models.BooleanField(default=True, help_text="Show in public project list")
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class ProjectFile(models.Model):
    """Code files and assets for projects"""
    
    FILE_TYPE_CHOICES = (
        ('code', 'Code'),
        ('doc', 'Documentation'),
        ('image', 'Image'),
        ('video', 'Video'),
        ('other', 'Other'),
    )
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='files')
    title = models.CharField(max_length=200)
    file_type = models.CharField(max_length=20, choices=FILE_TYPE_CHOICES, default='code')
    
    # For code files
    language = models.CharField(
        max_length=50,
        blank=True,
        help_text="Programming language (Python, JavaScript, etc.)"
    )
    code_content = models.TextField(blank=True, help_text="For code snippets")
    
    # For file uploads
    file = models.FileField(upload_to='project_files/', blank=True, null=True)
    
    # For links/resources
    external_url = models.URLField(blank=True, null=True, help_text="Link to external resource")
    
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.project.title} - {self.title}"


class ProjectUpdate(models.Model):
    """Updates/progress notes for projects"""
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='updates')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.project.title} - {self.title}"
