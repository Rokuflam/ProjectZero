"""
Tests for user models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
# pylint: disable=invalid-name


def create_user(email='user@example.com', password='Testpass123?'):
    """
    Create a new user with the given email and password.

    Parameters:
        email (str): The email address of the user. (default is 'user@example.com')
        password (str): The password for the user. (default is 'Testpass123?')

    Returns:
        User: The newly created user object.

    Example:
        create_user(email='john@example.com', password='SecurePassword123!')
    """
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """
    ModelTests is a class that contains test cases for the model functionality.
    """

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful"""
        email = 'test@example.com'
        password = 'Testpass666%#$?'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users"""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'sample123')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
