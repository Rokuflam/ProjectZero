from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from django.contrib.auth import get_user_model


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
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
                'full_name',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )


# Register the translation for the UserAdmin class
admin.site.register(get_user_model(), UserAdmin)
