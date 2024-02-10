from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from apps.core.utils import get_tokens_for_user

from .serializers import (
    UserSerializer,
    RetrieveUserSerializer,
)


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        user = get_user_model().objects.get(pk=serializer.data['id'])
        return Response(get_tokens_for_user(user), status=status.HTTP_201_CREATED, headers=headers)


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user

    def get_serializer_class(self):
        """Return the serializer class based on the request method."""
        if self.request.method in ['GET']:
            # Use a different serializer for get request
            return RetrieveUserSerializer
        else:
            # Use the default serializer for other request methods (e.g., PUT, PATCH)
            return self.serializer_class
