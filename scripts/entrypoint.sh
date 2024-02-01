#!/bin/sh

set -e

# Set the default value for DJANGO_SETTINGS_MODULE
DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-config.settings.development}

# Run Django management commands with the specified settings
python manage.py makemigrations --settings="$DJANGO_SETTINGS_MODULE" --no-input
python manage.py migrate --settings="$DJANGO_SETTINGS_MODULE" --no-input
python manage.py collectstatic --settings="$DJANGO_SETTINGS_MODULE" --no-input

# Run Gunicorn with the specified DJANGO_SETTINGS_MODULE
exec gunicorn --env DJANGO_SETTINGS_MODULE="$DJANGO_SETTINGS_MODULE" config.wsgi:application -b 0.0.0.0:8000 --reload
