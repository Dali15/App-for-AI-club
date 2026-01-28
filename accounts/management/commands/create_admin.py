from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a superuser account if it does not exist'

    def handle(self, *args, **options):
        # Check if superuser already exists
        if User.objects.filter(username='admin').exists():
            self.stdout.write(self.style.SUCCESS('✅ Superuser already exists'))
            return

        # Create superuser from environment variables or defaults
        username = os.getenv('ADMIN_USERNAME', 'admin')
        email = os.getenv('ADMIN_EMAIL', 'med2006dali@gmail.com')
        password = os.getenv('ADMIN_PASSWORD', 'admin123456')

        try:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(f'✅ Superuser "{username}" created successfully!'))
            self.stdout.write(f'   📧 Email: {email}')
            self.stdout.write(f'   🔐 Password: {password}')
            self.stdout.write(f'\n   Visit: https://ai-club-ssnk.onrender.com/admin')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error creating superuser: {str(e)}'))
