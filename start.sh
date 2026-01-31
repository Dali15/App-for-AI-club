#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Apply database migrations
echo "Runnning migrations..."
python manage.py migrate

# Create superuser if configured
echo "Checking for superuser creation..."
python create_superuser.py

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn
echo "Starting Gunicorn..."
gunicorn ai_club.wsgi:application
