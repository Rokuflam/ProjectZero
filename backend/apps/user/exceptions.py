"""
This module contains a custom exception class for handling user registration conflicts.
"""
from rest_framework.exceptions import APIException


class UserAlreadyExistsException(APIException):
    """
    A custom exception class that is raised when a user already exists.

    Attributes:
        status_code (int): The HTTP status code for conflict (409).
        default_detail (str): The default detail message ('User already exists').
        default_code (str): The default error code ('user_exists').

    """
    status_code = 409  # HTTP status code for conflict
    default_detail = 'User already exists'
    default_code = 'user_exists'
