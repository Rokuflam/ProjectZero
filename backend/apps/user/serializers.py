from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class RetrieveUserSerializer(UserSerializer):
    """Serializer for retrieving data from user object."""

    class Meta(UserSerializer.Meta):
        fields = [
            'id', 'email', 'username', 'full_name', 'avatar', 'last_login',
            'date_joined', 'role', 'is_active', 'is_staff'
        ]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Serializer for the obtaining token"""
    def validate(self, attrs):
        # The default result (access/refresh tokens)
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)

        # Custom data you want to include
        # data.update({'id': self.user.id})
        # and everything else you want to send in the response
        return data
