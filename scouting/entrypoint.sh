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

User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    import os
    username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
    email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
    password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'password123')
    
    User.objects.create_superuser(username, email, password)
    print("Superuser created successfully.")
else:
    print("Superuser already exists. Skipping creation.")
EOF

exec "$@"

