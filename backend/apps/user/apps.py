"""
APP Config for user application.
"""
from django.apps import AppConfig


class UserConfig(AppConfig):
    """UserConfig class

    This class represents the configuration for the user app in a Django project.

    Attributes:
        default_auto_field (str): The default auto field to use for models in the user app.
        name (str): The name of the user app.

    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.user'
