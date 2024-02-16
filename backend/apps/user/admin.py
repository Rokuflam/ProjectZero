"""
Admin panel settings for User model
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from django.contrib.auth import get_user_model


class UserAdmin(BaseUserAdmin):
    """

    This class represents the UserAdmin with extended functionality
     for managing user accounts in the application.

    Attributes:
        ordering (list): A list of fields to specify the default ordering of user records.
        list_display (list): A list of fields to be displayed in the user list view.
        fieldsets (tuple): A tuple of fieldset sections for organizing fields in the user detail view.
        readonly_fields (list): A list of fields that are read-only in the user detail view.
        add_fieldsets (tuple): A tuple of fieldset sections for organizing fields in the user creation view.

    Example Usage:
        user_admin = UserAdmin()

    Note:
        This class extends the BaseUserAdmin class.

    """
    ordering = ['id']
    list_display = ['email', 'full_name', 'last_login']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Account Details'),
            {
                'fields': (
                    'first_name',
                    'last_name',
                    'avatar',
                    'role',
                )
             }
        ),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ['last_login', 'date_joined']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'first_name',
                'last_name',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )


# Register the translation for the UserAdmin class
admin.site.register(get_user_model(), UserAdmin)
