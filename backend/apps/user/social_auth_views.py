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


class UserInfoFetcher:
    """
    Fetches user information from the given user_info_url using an HTTP GET request.
    """
    def fetch_user_info(self, user_info_url: str, headers: dict = None, params: dict = None) -> dict:
        """
        Fetches user information from the specified URL using an HTTP GET request.

        :param user_info_url: The URL to fetch the user information from.
        :param headers: (optional) Additional headers to include in the request.
        :param params: (optional) Additional query parameters to include in the request.
        :return: A dictionary containing the user information.
        :raises: An exception if the response status code is not 200.
        """
        response = requests.get(user_info_url, headers=headers, params=params, timeout=10)

        if response.status_code != 200:
            self.handle_error(response)

        return response.json()

    def handle_error(self, response):
        """
        Handle Error

        Handles error in the response by raising an Exception.

        Parameters:
        - self: The instance of the class.
        - response: The response object.

        Raises:
        - Exception: If there is a failure in fetching user info.
        """
        raise Exception(
            f"Failed to fetch user info. Status code: {response.status_code}, Response: {response.text}"
        )


class GoogleUserInfoFetcher(UserInfoFetcher):
    """
    Class GoogleUserInfoFetcher

    Class for fetching user information from Google.

    Inherits from UserInfoFetcher.
    """
    def fetch_user_info(self, token: str):
        """
        Fetches user information from Google API using the provided OAuth token.

        :param token: The OAuth token for authentication.
        :type token: str
        :return: A dictionary containing user information.
        :rtype: dict

        Example usage:
            >>> token = "some_oauth_token"
            >>> user_info = fetch_user_info()
            >>> print(user_info)
            {'id': '1234567890', 'first_name': 'John', 'last_name': 'Doe', 'email': 'john.doe@example.com'}
        """
        google_user_info_url = "https://www.googleapis.com/oauth2/v3/userinfo"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = super().fetch_user_info(google_user_info_url, headers)
        key_mapping = {'sub': 'id', 'given_name': 'first_name', 'family_name': 'last_name', 'email': 'email'}
        new_dict = {}
        for k, v in response.items():
            # Replace the key if it's in the mapping, otherwise keep the original key
            new_key = key_mapping.get(k, k)
            new_dict[new_key] = v
        return new_dict


class FacebookUserInfoFetcher(UserInfoFetcher):
    """
    Class FacebookUserInfoFetcher

    Class for fetching user information from Facebook.

    Inherits from UserInfoFetcher.
    """
    def fetch_user_info(self, token: str):
        """

        Fetch User Info

        This method fetches the user information from Facebook using the provided access token.

        Parameters:
        - token (str): Access token required to authenticate and authorize the request.

        Returns:
        - User Info (dict): A dictionary containing the user information fetched from Facebook.

        """
        facebook_user_info_url = "https://graph.facebook.com/v9.0/me"
        params = {
            "fields": "id,name,first_name,last_name,email",
            "access_token": token,
        }
        return super().fetch_user_info(facebook_user_info_url, params=params)


class SocialLoginView(APIView):
    """
    The SocialLoginView class is a view that handles social login functionality.
    It is an APIView subclass and provides a POST method for handling social login requests.
    """
    def __init__(self, **kwargs):
        """
        Initializes the object with the specified keyword arguments.

        Parameters:
        - `kwargs` (dict): A dictionary of keyword arguments.

        Returns:
        None
        """
        super().__init__(**kwargs)
        self.provider = 'test'
        self.fetcher = GoogleUserInfoFetcher()

    @extend_schema(
        request=TokenSerializer,
    )
    def post(self, request):
        """
        Post method for handling the token authentication for social login.

        Parameters:
        - request: The HTTP request object containing the data.

        Return Type:
        - Response: The HTTP response object.

        Example Usage:
            response = post(request)
        """
        token = request.data.get('token')
        if not self.is_token_present(token):
            return Response({'error': 'Token not provided'}, status=status.HTTP_400_BAD_REQUEST)

        social_login = self.get_or_create_social_login(self.provider, token)
        if not self.is_login_successful_for_provider(social_login):
            return Response({'error': F'Error with {self.provider.capitalize()} login'},
                            status=status.HTTP_400_BAD_REQUEST)

        self.authenticate_user(social_login, request)

        if not request.user.is_authenticated:
            return Response({'error': 'Authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)

        return self.create_auth_token_response(request)

    def get_or_create_social_login(self, provider, token):
        """

        Method: get_or_create_social_login

        Description:
        This method is used to get or create a social login for a user.

        Parameters:
        - provider (str): The provider of the social login.
        - token (str): The authentication token for the social login.

        Returns:
        - social_login (object): The created or existing social login for the user.
        Returns None if the SocialApp does not exist.

        """
        try:
            app, user_info, user, account = self.get_login_data(provider, token)
            social_token = self.create_or_update_social_token(app, account, token)
            social_login = self.create_social_login(user, account, social_token, user_info)

            return social_login
        except SocialApp.DoesNotExist:
            return None

    def get_login_data(self, provider, token):
        """
        Get login data for a given provider and token.

        Parameters:
        - provider (str): The provider name.
        - token (str): The token used for authentication.

        Returns:
        - app (SocialApp): The social app associated with the provider.
        - user_info (dict): Information about the user obtained from the provider.
        - user (User): The user object created or retrieved from the database.
        - account (SocialAccount): The social account associated with the user.

        Example usage:
            provider = 'google'
            token = 'abc123'
            app, user_info, user, account = get_login_data(provider, token)
        """
        app = SocialApp.objects.get(provider=provider)
        user_info = self.fetcher.fetch_user_info(token)
        user, _ = get_user_model().objects.get_or_create(email=user_info['email'], defaults={
            'username': user_info['email'],
            'first_name': user_info['first_name'],
            'last_name': user_info['last_name'],
        })
        account, _ = SocialAccount.objects.get_or_create(
            provider=provider, uid=user_info['id'], defaults={'extra_data': user_info, 'user': user}
        )
        return app, user_info, user, account

    def is_token_present(self, token):
        """
        Check if a token is present.

        Parameters:
        token (Any): The token to check.

        Returns:
        bool: True if the token is present, False otherwise.
        """
        return bool(token)

    def is_login_successful_for_provider(self, social_login):
        """
        Checks if the login was successful for the given provider.

        Parameters:
        - self: The instance of the class that the method is being called on.
        - social_login: A variable representing the social login attempt.

        Returns:
        - True if the login was successful, False otherwise.

        """
        return bool(social_login)

    def authenticate_user(self, social_login, request):
        """
        Authenticates the user using social login information.

        Args:
            social_login (SocialLogin): The social login object containing the user's social login info.
            request (HttpRequest): The Django HTTP request object.

        Returns:
            None

        Raises:
            None
        """
        if social_login.is_existing:
            login(request, social_login.user, backend='django.contrib.auth.backends.ModelBackend')
        else:
            request._request = HttpRequest()  # pylint: disable=protected-access
            complete_social_login(request._request, social_login)  # pylint: disable=protected-access

    def create_auth_token_response(self, request):
        """
        Create authentication token response.

        Parameters:
        - request: A request object containing user information.

        Returns:
        - A Response object containing a refresh token and an access token.
        """
        refresh = RefreshToken.for_user(request.user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

    def create_or_update_social_token(self, app, account, token):
        """Create or update a social token for a given app, account, and token.

        Parameters:
        - app (App): The app for which the social token is being created or updated.
        - account (Account): The account for which the social token is being created or updated.
        - token (str): The token value to be assigned to the social token.

        Returns:
        - social_token (SocialToken): The created or updated social token.

        Example:
        app = App.objects.get(id=1)
        account = Account.objects.get(id=1)
        token = 'example_token'
        social_token = create_or_update_social_token(app, account, token)
        """
        try:
            social_token = SocialToken.objects.get(app=app, account=account)
            social_token.token = token
            social_token.save()
        except SocialToken.DoesNotExist:
            social_token = SocialToken.objects.create(app=app, token=token, account=account)

        return social_token

    def create_social_login(self, user, account, social_token, user_info):
        """
        Create a social login instance.

        :param user: The associated user object.
        :type user: User

        :param account: The social account object.
        :type account: SocialAccount

        :param social_token: The social token string.
        :type social_token: str

        :param user_info: The user information dictionary.
        :type user_info: dict

        :return: The social login instance.
        :rtype: SocialLogin
        """
        return SocialLogin(
            user=user, account=account, token=social_token, email_addresses=[user_info['email']]
        )


class GoogleLoginView(SocialLoginView):
    """
    Class: GoogleLoginView

    Subclass of: SocialLoginView

    This class represents a view for logging in with Google on a website or application.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.provider = 'google'
        self.fetcher = GoogleUserInfoFetcher()


class FaceBookLoginView(SocialLoginView):
    """
    Class: FaceBookLoginView

    Subclass of: SocialLoginView

    This class represents a view for logging in with Facebook on a website or application.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.provider = 'facebook'
        self.fetcher = FacebookUserInfoFetcher()
