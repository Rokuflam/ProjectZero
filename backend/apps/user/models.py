"""
Database User related models
"""
import uuid
import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db.models.functions import Concat


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        # TODO: add more validation on fields
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    # TODO: recheck if all fields are set properly
    # TODO: Set in the settings AUTH_USER_MODEL
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(
        max_length=24,
        null=True,
        blank=False
    )
    last_name = models.CharField(
        max_length=24,
        null=True,
        blank=False
    )
    full_name = models.GeneratedField(
        expression=Concat("first_name", models.Value(" "), "last_name"),
        output_field=models.CharField(max_length=511),
        db_persist=True,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    ROLE_ADMIN = 'admin'
    ROLE_USER = 'user'
    ROLE_CHOICES = (
        (ROLE_ADMIN, 'Admin'),
        (ROLE_USER, 'User'),
    )
    role = models.CharField(max_length=256,
                            choices=ROLE_CHOICES, default=ROLE_USER)

    date_joined = models.DateField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = ['email', 'username']

    def __str__(self):
        return f"email: {self.email} username: {self.username}"
