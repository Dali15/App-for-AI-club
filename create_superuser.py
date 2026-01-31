import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_club.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Create superuser with credentials from environment or defaults
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'Admin123!')

if not User.objects.filter(username=username).exists():
    print(f"Creating superuser '{username}'...")
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"✅ Superuser '{username}' created successfully!")
    print(f"   Email: {email}")
    print(f"   Password: {password[:2]}****{password[-2:]} (masked)")
else:
    print(f"⚠️  Superuser '{username}' already exists. Skipping creation.")

