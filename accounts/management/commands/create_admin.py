from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Create or update a superuser account'

    def handle(self, *args, **options):
        # Get credentials from environment variables
        username = os.getenv('ADMIN_USERNAME', 'admin')
        email = os.getenv('ADMIN_EMAIL', 'med2006dali@gmail.com')
        password = os.getenv('ADMIN_PASSWORD', 'admin123456')

        try:
            # Check if user already exists
            user = User.objects.filter(username=username).first()
            
            if user:
                # Update existing user's password and email
                user.email = email
                user.set_password(password)
                user.is_superuser = True
                user.is_staff = True
                user.save()
                self.stdout.write(self.style.SUCCESS(f'✅ Superuser "{username}" updated!'))
                self.stdout.write(f'🔐 Password has been reset')
            else:
                # Create new superuser
                user = User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )
                self.stdout.write(self.style.SUCCESS(f'✅ Superuser "{username}" created!'))
            
            self.stdout.write(f'📧 Email: {email}')
            self.stdout.write(f'🔐 Password: {password}')
            self.stdout.write(f'\n📍 Login at: https://ai-club-ssnk.onrender.com/admin')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error: {str(e)}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error: {str(e)}'))
