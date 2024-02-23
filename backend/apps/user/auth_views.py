from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from allauth.socialaccount.helpers import complete_social_login
from allauth.socialaccount.models import SocialLogin, SocialToken, SocialApp
from django.http import HttpRequest

from .serializers import TokenSerializer

User = get_user_model()


def get_social_login(provider, token):
    try:
        app = SocialApp.objects.get(provider=provider)
        social_token = SocialToken(app=app, token=token)
        login = SocialLogin(token=social_token)
        return login
    except SocialApp.DoesNotExist:
        return None


class SocialLoginView(APIView):
    permission_classes = [AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.provider = 'test'

    @extend_schema(
        request=TokenSerializer,  # Specify the custom serializer for the request body
    )
    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token not provided'}, status=400)
        social_login = get_social_login(self.provider, token)
        if not social_login:
            return Response({'error': 'Error with {} login'.format(self.provider.capitalize())}, status=400)
        request._request = HttpRequest()
        complete_social_login(request._request, social_login)
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication failed'}, status=401)
        refresh = RefreshToken.for_user(request.user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


class GoogleLoginView(SocialLoginView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.provider = 'google'


class FaceBookLoginView(SocialLoginView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.provider = 'facebook'
