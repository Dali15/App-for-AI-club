# Docker Configuration
# For local testing or advanced deployments

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput --clear

# Run migrations and start server
CMD ["sh", "-c", "python manage.py migrate && gunicorn ai_club.wsgi:application --bind 0.0.0.0:$PORT"]
