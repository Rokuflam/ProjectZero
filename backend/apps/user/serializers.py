"""
Serializers for User models
"""
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    """
    Class: UserSerializer

    The UserSerializer class is used for serializing and deserializing user data.
     It is a subclass of the ModelSerializer class provided by the Django REST Framework.

    Attributes:
    - model (Model): The Django model associated with this serializer.
    - fields (list): A list of fields to include in the serialized representation.
    - extra_kwargs (dict): Additional keyword arguments for customizing field behavior.

    Methods:
    - create(self, validated_data): Creates and returns a user with encrypted password.
    - update(self, instance, validated_data): Updates and returns a user.

    Example usage:

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.create(validated_data=serializer.validated_data)
            # do something with the user object

    """

    class Meta:
        """
        model (Model): The Django model associated with this serializer.
        fields (list): A list of fields to include in the serialized representation.
        extra_kwargs (dict): Additional keyword arguments for customizing field behavior.
            For example, {'password': {'write_only': True, 'min_length': 5}}.
        """
        model = get_user_model()
        fields = [
            'id', 'email', 'password', 'username', 'full_name', 'avatar',
            'last_login', 'date_joined', 'role'
        ]
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


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """

    CustomTokenObtainPairSerializer class extends the TokenObtainPairSerializer class.

    This class is used for validating the attributes passed to the serializer's validate() method.
     It adds custom data to the response data.

    Methods:
    - validate(attrs): This method is called when the serializer
     is validating the provided attributes. It first calls the validate() method
      of the parent class (TokenObtainPairSerializer
    *) to get the default result (access/refresh tokens).
     Then, it adds custom data to the response data and returns it.

    Example usage:
    serializer = CustomTokenObtainPairSerializer(data=request.data)
    if serializer.is_valid():
        response = serializer.validated_data
        # Do something with the response data

    Note: To include custom data in the response, uncomment the line
    'data.update({'id': self.user.id})' and add any additional data you want to include.

    """
    def validate(self, attrs):
        """validate the attributes passed to the serializer"""
        # The default result (access/refresh tokens)
        data = super().validate(attrs)

        # Custom data you want to include
        # data.update({'id': self.user.id})
        # and everything else you want to send in the response
        return data


# Schemas serializers
class TokenSerializer(serializers.Serializer):
    """
    Class for serializing authentication tokens.

    Attributes:
        token (serializers.CharField): Required field representing the authentication token.
    """
    token = serializers.CharField(required=True, help_text="Authentication token")
