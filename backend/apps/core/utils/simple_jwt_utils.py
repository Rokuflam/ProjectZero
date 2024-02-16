"""
This module provides utility functions for working with JWT (JSON Web Tokens) using the `simple_jwt` library.
"""
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    """
    Generate JWT refresh and access tokens for a specific user.

    :param user: User instance for which tokens will be generated
    :return:
    A dictionary with 'refresh' and 'access' keys containing JWT refresh and access tokens respectively
    """
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }
