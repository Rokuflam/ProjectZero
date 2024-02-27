"""
This is a test module for testing the user model's admin interface modifications in Django.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from apps.core.utils import get_tokens_for_user
# pylint: disable=invalid-name

CREATE_USER_URL = reverse('user:create')
TOKEN_OBTAIN_URL = reverse('user:token_obtain_pair')
TOKEN_REFRESH_URL = reverse('user:token_refresh')
TOKEN_VERIFY_URL = reverse('user:token_verify')
ME_URL = reverse('user:me')


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Tests the public features of the user API."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """Test error return if the user with email exists."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is returned if password less than 5 chars."""
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_retrieve_user_authenticated(self):
        """Test authentication is required for users."""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class TokenUserApiTests(TestCase):
    """Tests the jwt token features of the user API."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.user_details = {
            'email': 'test@example.com',
            'password': 'test-user-password123'
        }
        self.user = create_user(**self.user_details)
        self.client = APIClient()

    def test_obtain_token_for_user(self):
        """Test generates token for valid credentials."""
        payload = {
            'email': self.user_details['email'],
            'password': self.user_details['password'],
        }
        res = self.client.post(TOKEN_OBTAIN_URL, payload)

        self.assertIn('refresh', res.data)
        self.assertIn('access', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_obtain_token_bad_credentials(self):
        """Test returns error if credentials invalid."""
        payload = {
            'email': self.user_details['email'],
            'password': 'badpass',
        }
        res = self.client.post(TOKEN_OBTAIN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_obtain_token_blank_password(self):
        """Test posting a blank password return an error."""
        payload = {
            'email': self.user_details['email'],
            'password': '',
        }
        res = self.client.post(TOKEN_OBTAIN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_verify_token(self):
        """Test posting a valid token"""
        old_token = get_tokens_for_user(self.user)
        payload = {
            'token': old_token['access']
        }

        res = self.client.post(TOKEN_VERIFY_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_verify_token_bad_credentials(self):
        """Test returns error if credentials invalid."""
        get_tokens_for_user(self.user)
        payload = {
            'token': 'invalid_token'
        }

        res = self.client.post(TOKEN_VERIFY_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token_for_user(self):
        """Test refresh token for valid credentials."""
        old_token = get_tokens_for_user(self.user)
        payload = {
            'refresh': old_token['refresh']
        }

        res = self.client.post(TOKEN_REFRESH_URL, payload)
        self.assertIn('access', res.data)
        self.assertNotEqual(old_token['access'], res.data['access'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_refresh_token_bad_credentials(self):
        """Test returns error if credentials invalid."""
        get_tokens_for_user(self.user)
        payload = {
            'refresh': 'invalid_token'
        }

        res = self.client.post(TOKEN_REFRESH_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requirements that require authentication."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.user_details = {
            'email': 'test@example.com',
            'password': 'test-user-password123',
            "username": "GregZero",
            "first_name": "Me",
            "last_name": "Best",
        }
        self.user = create_user(**self.user_details)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user."""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_post_me_not_allowed(self):
        """Test POST is not allowed for the me endpoint."""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for the authenticated user."""
        payload = {'username': 'Updated bro', 'email': 'update@email.com'}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.username, payload['username'])
        self.assertEqual(self.user.email, payload['email'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)
