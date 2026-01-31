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
    print(f"Creating superuser '{username}'...", flush=True)
    User.objects.create_superuser(username=username, email=email, password=password, role='owner')
    print(f"✅ Superuser '{username}' created successfully!", flush=True)
else:
    print(f"⚠️  User '{username}' already exists. Updating credentials...", flush=True)
    user = User.objects.get(username=username)
    user.set_password(password)
    user.email = email
    user.is_staff = True
    user.is_superuser = True
    user.role = 'owner'
    user.save()
    print(f"✅ User '{username}' updated! Password reset, promoted to superuser & role set to Owner.", flush=True)

print(f"   Email: {email}", flush=True)
print(f"   Password: {password[:2]}****{password[-2:]} (masked)", flush=True)

