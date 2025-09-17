#!/bin/bash

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Build binary translation files
python manage.py compilemessages

# Create super user
echo "Checking if a superuser already exists..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
from authentication.models import Profile, Settings
import os

User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
    email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
    password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'password123')
    display_name = os.getenv('DJANGO_SUPERUSER_PROFILE_DISPLAY_NAME', 'Admin')
    team_number = os.getenv('DJANGO_SUPERUSER_PROFILE_TEAM_NUMBER', '0000')
    
    user = User.objects.create_superuser(username, email, password)

    profile = Profile(user=user, display_name=display_name, team_number=team_number)
    profile.save()

    settings = Settings(user=user)
    settings.save()

    print("Superuser and profile created successfully.")
else:
    print("Superuser already exists. Skipping creation.")
EOF

exec "$@"

