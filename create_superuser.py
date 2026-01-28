#!/usr/bin/env python
"""
Script to create a superuser for Render deployment
Run this once to create the admin account
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_club.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Create superuser with your credentials
username = 'admin'
email = 'med2006dali@gmail.com'
password = 'ChangeMe123!'  # CHANGE THIS!

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"✅ Superuser '{username}' created successfully!")
    print(f"   Email: {email}")
    print(f"   Password: {password}")
    print(f"\n   Visit: https://ai-club-ssnk.onrender.com/admin")
    print(f"   Login with your credentials above")
else:
    print(f"⚠️  Superuser '{username}' already exists!")
