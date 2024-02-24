import requests
from django.contrib.auth import get_user_model, login
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from allauth.socialaccount.helpers import complete_social_login
from allauth.socialaccount.models import SocialLogin, SocialToken, SocialApp, SocialAccount
from django.http import HttpRequest

from .serializers import TokenSerializer

User = get_user_model()

# TODO: Linting, Fixtures for social appliacations + sites
def fetch_user_info_from_google(token):
    """Fetch user information from Google's OAuth 2.0 API using the provided access token."""
    google_user_info_url = "https://www.googleapis.com/oauth2/v3/userinfo"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(google_user_info_url, headers=headers)

    if response.status_code == 200:
        response = response.json()
        key_mapping = {'sub': 'id', 'given_name': 'first_name', 'family_name': 'last_name', 'email': 'email'}

        new_dict = {}
        for k, v in response.items():
            # Replace the key if it's in the mapping, otherwise keep the original key
            new_key = key_mapping.get(k, k)
            new_dict[new_key] = v
        return new_dict  # Return the user information as a dictionary
    else:
        # Handle error responses appropriately
        raise Exception(
            f"Failed to fetch user info from Google. Status code: {response.status_code}, Response: {response.text}")


def fetch_user_info_from_facebook(token):
    """Fetch user information from Facebook's Graph API using the provided access token."""
    facebook_user_info_url = "https://graph.facebook.com/v9.0/me"
    params = {
        "fields": "id,name,first_name,last_name,email,picture{url}",
        "access_token": token,
    }
    response = requests.get(facebook_user_info_url, params=params)

    if response.status_code == 200:
        return response.json()  # Return the user information as a dictionary
    else:
        # Handle error responses appropriately
        raise Exception(
            f"Failed to fetch user info from Facebook. Status code: {response.status_code}, Response: {response.text}")


class SocialLoginView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.provider = 'test'
        self.fetch_user_info = None

    @extend_schema(
        request=TokenSerializer,  # Specify the custom serializer for the request body
    )
    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token not provided'}, status=400)
        social_login = self.get_social_login(self.provider, token)

        if not social_login:
            return Response({'error': 'Error with {} login'.format(self.provider.capitalize())}, status=400)
        # Check if social_login represents an existing user
        if social_login.is_existing:
            # Perform login for existing user
            login(request, social_login.user, backend='django.contrib.auth.backends.ModelBackend')
        else:
            # Complete the signup process for new users
            request._request = HttpRequest()
            complete_social_login(request._request, social_login)

        if not request.user.is_authenticated:
            return Response({'error': 'Authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(request.user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

    def get_social_login(self, provider, token):
        try:
            app = SocialApp.objects.get(provider=provider)
            user_info = self.fetch_user_info(token)  # Make sure this function correctly fetches user info
            user, _ = get_user_model().objects.get_or_create(email=user_info['email'], defaults={
                'username': user_info['email'],
                'first_name': user_info['first_name'],
                'last_name': user_info['last_name'],
            })

            account, _ = SocialAccount.objects.get_or_create(provider=provider, uid=user_info['id'], defaults={
                'extra_data': user_info, 'user': user
            })

            # Check if a SocialToken for this app and account already exists
            try:
                social_token = SocialToken.objects.get(app=app, account=account)
                # If it does, update the token value
                social_token.token = token
                social_token.save()
            except SocialToken.DoesNotExist:
                # If it doesn't exist, create a new SocialToken
                social_token = SocialToken.objects.create(app=app, token=token, account=account)

            login = SocialLogin(user=user, account=account, token=social_token,
                                email_addresses=[user_info['email']])  # Directly pass the SocialToken instance
            return login
        except SocialApp.DoesNotExist:
            return None


class GoogleLoginView(SocialLoginView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.provider = 'google'
        self.fetch_user_info = fetch_user_info_from_google


class FaceBookLoginView(SocialLoginView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.provider = 'facebook'
        self.fetch_user_info = fetch_user_info_from_facebook
