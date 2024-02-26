#!/bin/sh

set -e

# Set the default value for DJANGO_SETTINGS_MODULE
DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-config.settings.development}

# Run Django management commands with the specified settings
python manage.py wait_for_db --settings="$DJANGO_SETTINGS_MODULE"
python manage.py makemigrations --settings="$DJANGO_SETTINGS_MODULE" --no-input
python manage.py collectstatic --settings="$DJANGO_SETTINGS_MODULE" --no-input
python manage.py migrate --settings="$DJANGO_SETTINGS_MODULE"
python manage.py loaddata --settings="$DJANGO_SETTINGS_MODULE" user social-auth

# Run Uvicorn with the specified DJANGO_SETTINGS_MODULE
export DJANGO_SETTINGS_MODULE="$DJANGO_SETTINGS_MODULE"
exec uvicorn config.asgi:application --host 0.0.0.0 --port 8000 --reload