from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Synchronizes permissions for all users based on their roles'

    def handle(self, *args, **options):
        self.stdout.write('Syncing user roles and permissions...')
        users = User.objects.all()
        count = 0
        for user in users:
            # Saving the user triggers the post_save signal
            # which enforces the role permissions
            user.save()
            count += 1
            
        self.stdout.write(self.style.SUCCESS(f'Successfully synced permissions for {count} users'))
