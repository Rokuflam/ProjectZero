"""
URL mapping for the user API.
"""
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from apps.user import views
from .auth_views import google_login, facebook_login
app_name = 'user'  # pylint: disable=invalid-name

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('me/', views.ManageUserView.as_view(), name='me'),
path('social/google/', google_login, name='google_login'),
    path('social/facebook/', facebook_login, name='facebook_login'),
]
