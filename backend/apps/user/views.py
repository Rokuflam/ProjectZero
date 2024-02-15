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
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction

# Django Rest Framework imports
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

# Local modules import
from .exceptions import UserAlreadyExistsException
from .serializers import UserSerializer
from apps.core.utils import get_tokens_for_user


class CreateUserView(generics.CreateAPIView):
    """API view to create a new user in the system."""
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        """
        Creates a new user upon POST request.

        Args:
            request (rest_framework.request.Request): The request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            rest_framework.response.Response: Response with token details if the user creation is successful.
        """
        # Validate and transform input data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check if the user already exists
        User = get_user_model()
        if User.objects.filter(username=request.data.get('username')).exists():
            raise UserAlreadyExistsException("User already exists.")

            # Perform the creation operation in a database transaction
        try:
            with transaction.atomic():
                self.perform_create(serializer)
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Fetch user and generate tokens
        headers = self.get_success_headers(serializer.data)
        user = User.objects.get(pk=serializer.data['id'])

        return Response(
            get_tokens_for_user(user),
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class ManageUserView(generics.RetrieveUpdateAPIView):
    """API view to manage the authenticated user."""
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
