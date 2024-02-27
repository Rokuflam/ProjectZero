"""
This file contains the APIView classes for creating and managing users.

Modules:
    django.conf: Contains the settings for the Django project.
    django.contrib.auth: A Django module that manages the authentication process.
    rest_framework: Django Rest_Framework that provides features for building web APIs.
    rest_framework.response: Module that handles sending API responses.
    apps.core.utils: Custom module that contains utility functions like `get_tokens_for_user`.
    serializers: Module in the same directory, that holds the serializer for User object.

Classes:
    CreateUserView: API View to register a new user into the system.
    ManageUserView: API View to retrieve or update the authenticated user's details.
"""

# Django Standard Library Imports
from django.contrib.auth import get_user_model
from django.db import transaction

# Django Rest Framework imports
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

# Local modules import
from apps.core.utils import get_tokens_for_user
from .exceptions import UserAlreadyExistsException
from .serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """

    CreateUserView

        This class is a view for creating new users upon receiving a POST request.

    Attributes:
        serializer_class (class): The class used for serializing the user data.

    Methods:
        create(self, request, *args, **kwargs)
        user_exists(user_model, username)
        get_user_tokens(user_model, user_id)

    """
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        """
        Creates a new user upon POST request.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = request.data.get('email')
        user_model = get_user_model()

        if self.user_exists(user_model, email):
            raise UserAlreadyExistsException("User already exists.")

        try:
            with transaction.atomic():
                self.perform_create(serializer)
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        headers = self.get_success_headers(serializer.data)
        tokens = self.get_user_tokens(user_model, serializer.data['id'])

        return Response(
            tokens,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    @staticmethod
    def user_exists(user_model, email):
        """
        Check if a user with the given email exists in the user model.
        """
        return user_model.objects.filter(email=email).exists()

    @staticmethod
    def get_user_tokens(user_model, user_id):
        """
        Static method to retrieve tokens for a given user.
        """
        user = user_model.objects.get(pk=user_id)
        return get_tokens_for_user(user)


class ManageUserView(generics.RetrieveUpdateAPIView):
    """
    A class representing the view for managing user information.
    """
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Retrieve and return authenticated user.

        Returns:
            obj: A user instance.
        """
        return self.request.user
