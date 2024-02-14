"""
APP Config for user application.
"""
from django.apps import AppConfig


class UserConfig(AppConfig):
    """
        Define the config for user application
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.user'
