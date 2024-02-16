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
    """A custom user manager class that extends the base UserManager class.

    This class provides methods to create and save new users, as well as create
    superusers.

    Attributes:
        None

    Methods:
        create_user(email, password=None, **kwargs): Create, save, and return a new user.
        create_superuser(email, password, **kwargs): Create and return a new superuser.
    """

    def create_user(self, email, password=None, **kwargs):
        """Create, save and return a new user."""
        if not email:
            raise ValueError(_('User must have an email address.'))
        email = self.normalize_email(email)

        user = self.model(email=email, **kwargs)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **kwargs):
        """Create and return a new superuser."""
        user = self.create_user(email, password, **kwargs)

        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    This class represents a User in the application.

    Attributes:
        id (UUIDField): The unique identifier for the user.
        email (EmailField): The email address of the user.
        username (CharField): The username of the user.
        avatar (ImageField): The avatar image of the user.
        first_name (CharField): The first name of the user.
        last_name (CharField): The last name of the user.
        full_name (GeneratedField): The generated field for the full name of the user.
        is_active (BooleanField): Indicates whether the user is active or not.
        is_staff (BooleanField): Indicates whether the user is a staff member or not.
        role (CharField): The role of the user.
        date_joined (DateField): The date when the user joined the application.
        objects (CustomUserManager): The manager for the User model.

    Methods:
        __str__(): Returns a string representation of the user object.

    Meta:
        This class also defines metadata options for the User model.

        Attributes:
            indexes (list): A list of database indexes.
            verbose_name (str): A human-readable name for the model in singular form.
            verbose_name_plural (str): A human-readable name for the model in plural form.
    """
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
        """
            Metadata options for the User model.

            Attributes:
                indexes (list): A list of database indexes.
                verbose_name (str): A human-readable name for the model in singular form.
                verbose_name_plural (str): A human-readable name for the model in plural form.
        """
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['date_joined']),
        ]
        verbose_name = _('User')
        verbose_name_plural = _('Users')
