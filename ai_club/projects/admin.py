from django.contrib import admin
from .models import Project, ProjectFile, ProjectUpdate


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'created_by', 'created_at', 'is_public')
    list_filter = ('category', 'status', 'is_public', 'created_at')
    search_fields = ('title', 'description', 'created_by__username')
    filter_horizontal = ('members',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category')
        }),
        ('Links', {
            'fields': ('repository_url', 'documentation_url')
        }),
        ('Status & Visibility', {
            'fields': ('status', 'is_public')
        }),
        ('Team', {
            'fields': ('created_by', 'members')
        }),
    )
    readonly_fields = ('created_by', 'created_at', 'updated_at')


@admin.register(ProjectFile)
class ProjectFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'file_type', 'language', 'uploaded_by', 'uploaded_at')
    list_filter = ('file_type', 'language', 'project', 'uploaded_at')
    search_fields = ('title', 'project__title', 'description')
    readonly_fields = ('uploaded_by', 'uploaded_at')


@admin.register(ProjectUpdate)
class ProjectUpdateAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'author', 'created_at')
    list_filter = ('project', 'created_at')
    search_fields = ('title', 'content', 'project__title')
    readonly_fields = ('created_at',)
