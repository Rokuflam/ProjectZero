"""
APP Config for core application.
"""
from django.apps import AppConfig


class UserConfig(AppConfig):
    """
    Define the config for core application
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'
