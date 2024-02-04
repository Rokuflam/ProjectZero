"""
Database User related models
"""
import uuid

from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import (
    AbstractBaseUser,
    UserManager,
    PermissionsMixin,
)

from apps.core.db import ConcatOp


class CustomUserManager(UserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError(_('User must have an email address.'))
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create and return a new superuser."""
        user = self.create_user(email, password, **extra_fields)

        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    username = models.CharField(max_length=30, null=True, blank=True)
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        verbose_name=_('Avatar')
    )
    first_name = models.CharField(
        max_length=24,
        null=True,
        blank=False,
        verbose_name=_('First Name'),
    )
    last_name = models.CharField(
        max_length=24,
        null=True,
        blank=False,
        verbose_name=_('Last Name'),
    )
    full_name = models.GeneratedField(
        expression=ConcatOp("first_name", models.Value(" "), "last_name"),
        output_field=models.CharField(max_length=511),
        db_persist=True,
        verbose_name=_('Full Name'),
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    ROLE_ADMIN = 'admin'
    ROLE_USER = 'user'
    ROLE_CHOICES = (
        (ROLE_ADMIN, _('Admin')),
        (ROLE_USER, _('User')),
    )
    role = models.CharField(
        max_length=256,
        choices=ROLE_CHOICES,
        default=ROLE_USER,
        verbose_name=_('Role')
    )

    date_joined = models.DateField(
        auto_now_add=True,
        db_index=True,
        verbose_name=_('Date Joined')
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return f"email: {self.email} username: {self.username}"

    class Meta:
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['date_joined']),
        ]
        verbose_name = _('User')
        verbose_name_plural = _('Users')
