from django.core.management.base import BaseCommand
from accounts.models import RolePermission


class Command(BaseCommand):
    help = 'Initialize default role permissions'

    def handle(self, *args, **options):
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
            for feature, _ in RolePermission.FEATURE_CHOICES:
                obj, created = RolePermission.objects.get_or_create(
                    role=role,
                    feature=feature,
                    defaults={'can_perform': feature in features}
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created permission: {role} - {feature}'))
        
        self.stdout.write(self.style.SUCCESS('Successfully initialized role permissions'))
