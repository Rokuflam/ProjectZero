from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from allauth.socialaccount.helpers import complete_social_login
from allauth.socialaccount.models import SocialLogin, SocialToken, SocialApp
from allauth.socialaccount.providers.google.provider import GoogleProvider
from allauth.socialaccount.providers.facebook.provider import FacebookProvider
from django.http import HttpRequest

User = get_user_model()

def get_social_login(provider, token):
    try:
        # Create a Social Token instance
        app = SocialApp.objects.get(provider=provider)
        social_token = SocialToken(app=app, token=token)

        # Create a Social Login instance
        login = SocialLogin(token=social_token)
        return login
    except SocialApp.DoesNotExist:
        return None

@api_view(['POST'])
@permission_classes([AllowAny])
def google_login(request):
    # Extract the token sent by the client
    token = request.data.get('token')
    if not token:
        return Response({'error': 'Token not provided'}, status=400)

    # Attempt to login/register the user based on the Google token
    social_login = get_social_login('google', token)
    if not social_login:
        return Response({'error': 'Error with Google login'}, status=400)

    # Mimic the request object for complete_social_login
    request._request = HttpRequest()

    # Complete the social login process
    complete_social_login(request._request, social_login)

    if not request.user.is_authenticated:
        return Response({'error': 'Authentication failed'}, status=401)

    # Generate JWT tokens
    refresh = RefreshToken.for_user(request.user)

    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def facebook_login(request):
    # Similar process for Facebook
    token = request.data.get('token')
    if not token:
        return Response({'error': 'Token not provided'}, status=400)

    social_login = get_social_login('facebook', token)
    if not social_login:
        return Response({'error': 'Error with Facebook login'}, status=400)

    request._request = HttpRequest()
    complete_social_login(request._request, social_login)

    if not request.user.is_authenticated:
        return Response({'error': 'Authentication failed'}, status=401)

    refresh = RefreshToken.for_user(request.user)

    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })
