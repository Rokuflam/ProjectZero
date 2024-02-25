"""
This module provides social login functionality for a Django based web application.
"""
import requests
from django.contrib.auth import (
    get_user_model,
    login
)
from django.http import HttpRequest
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from allauth.socialaccount.helpers import complete_social_login
from allauth.socialaccount.models import (
    SocialLogin,
    SocialToken,
    SocialApp,
    SocialAccount
)

from .serializers import TokenSerializer
# pylint: disable=broad-exception-raised

User = get_user_model()

# TODO: Linting, Fixtures for social appliacations + sites


def fetch_user_info_from_google(token):
    """
    Fetches user information from Google using the provided token.
    """
    google_user_info_url = "https://www.googleapis.com/oauth2/v3/userinfo"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(google_user_info_url, headers=headers, timeout=10)

    if response.status_code == 200:
        response = response.json()
        key_mapping = {'sub': 'id', 'given_name': 'first_name', 'family_name': 'last_name', 'email': 'email'}

        new_dict = {}
        for k, v in response.items():
            # Replace the key if it's in the mapping, otherwise keep the original key
            new_key = key_mapping.get(k, k)
            new_dict[new_key] = v
        return new_dict  # Return the user information as a dictionary
    # Handle error responses appropriately
    raise Exception(f"Failed to fetch user info from Google."
                    f" Status code: {response.status_code}, Response: {response.text}")


def fetch_user_info_from_facebook(token):
    """
    Fetches user information from Facebook using the provided access token.
    """
    facebook_user_info_url = "https://graph.facebook.com/v9.0/me"
    params = {
        "fields": "id,name,first_name,last_name,email",
        "access_token": token,
    }
    response = requests.get(facebook_user_info_url, params=params, timeout=10)

    if response.status_code == 200:
        return response.json()  # Return the user information as a dictionary
    # Handle error responses appropriately
    raise Exception(f"Failed to fetch user info from Facebook."
                    f" Status code: {response.status_code}, Response: {response.text}")


class SocialLoginView(APIView):
    """
    SocialLoginView is a class that handles the social login functionality for a user.
     It extends the APIView class from the Django Rest Framework.

    Attributes:
        - provider: A string representing the social login provider. Default value is 'test'.
        - fetch_user_info: A function that fetches user information from the social login provider.
         Its implementation is not provided.

    Methods:
        - post(request): Handles the POST request for social login. It requires a token in the request body.
         It checks if the token is provided, performs the social login process for an
    * existing user or completes the signup process for new users,
     and returns a response with refresh and access tokens upon successful authentication.
     If authentication fails, it returns
    * a response with an error message.
        - get_social_login(provider, token): Retrieves or creates a
         SocialLogin instance based on the provider and token.
         It fetches user information based on the token, creates or retrieves
    * a user account, associates the account with the provider, and creates or updates the SocialToken.
    It returns the SocialLogin instance.

    Note: The implementation of fetch_user_info and other related classes (
    TokenSerializer, SocialApp, SocialAccount, SocialToken, get_user_model, HttpRequest
    ) are not provided in the given * code.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.provider = 'test'
        self.fetch_user_info = fetch_user_info_from_google

    @extend_schema(
        request=TokenSerializer,  # Specify the custom serializer for the request body
    )
    def post(self, request):
        """
        This method is used to handle the HTTP POST request for social login.
        """
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token not provided'}, status=400)
        social_login = self.get_social_login(self.provider, token)

        if not social_login:
            return Response({'error': F'Error with {self.provider.capitalize()} login'}, status=400)
        # Check if social_login represents an existing user
        if social_login.is_existing:
            # Perform login for existing user
            login(request, social_login.user, backend='django.contrib.auth.backends.ModelBackend')
        else:
            # Complete the signup process for new users

            request._request = HttpRequest()  # pylint: disable=protected-access
            complete_social_login(request._request, social_login)  # pylint: disable=protected-access

        if not request.user.is_authenticated:
            return Response({'error': 'Authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(request.user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

    def get_social_login(self, provider, token):
        """
            Get social login information for a given provider and token.

            Args:
                provider (str): The name of the social provider.
                token (str): The authentication token from the social provider.

            Returns:
                SocialLogin or None: A SocialLogin instance representing the user's social login information,
                                     or None if the social app does not exist.

            Raises:
                None.
        """
        try:
            app = SocialApp.objects.get(provider=provider)
            user_info = self.fetch_user_info(token)  # Make sure this function correctly fetches user info
            user, _ = get_user_model().objects.get_or_create(email=user_info['email'], defaults={
                'username': user_info['email'],
                'first_name': user_info['first_name'],
                'last_name': user_info['last_name'],
            })

            account, _ = SocialAccount.objects.get_or_create(
                provider=provider, uid=user_info['id'], defaults={'extra_data': user_info, 'user': user}
            )

            # Check if a SocialToken for this app and account already exists
            try:
                social_token = SocialToken.objects.get(app=app, account=account)
                # If it does, update the token value
                social_token.token = token
                social_token.save()
            except SocialToken.DoesNotExist:
                # If it doesn't exist, create a new SocialToken
                social_token = SocialToken.objects.create(app=app, token=token, account=account)

            social_login = SocialLogin(
                user=user, account=account, token=social_token, email_addresses=[user_info['email']]
            )  # Directly pass the SocialToken instance
            return social_login
        except SocialApp.DoesNotExist:
            return None


class GoogleLoginView(SocialLoginView):
    """
    Class: GoogleLoginView

    Subclass of: SocialLoginView

    This class represents a view for logging in with Google on a website or application.

    Attributes:
    - provider: A string representing the name of the login provider (Google).
    - fetch_user_info: A function that fetches user information from the Google API.

    Methods:
    - __init__(self, **kwargs): Initializes an instance of the GoogleLoginView class.

    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.provider = 'google'
        self.fetch_user_info = fetch_user_info_from_google


class FaceBookLoginView(SocialLoginView):
    """
    Class: FaceBookLoginView

    Subclass of: SocialLoginView

    This class represents a view for logging in with Facebook on a website or application.

    Attributes:
    - provider: A string representing the name of the login provider (Facebook).
    - fetch_user_info: A function that fetches user information from the Facebook API.

    Methods:
    - __init__(self, **kwargs): Initializes an instance of the FaceBookLoginView class.

    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.provider = 'facebook'
        self.fetch_user_info = fetch_user_info_from_facebook
