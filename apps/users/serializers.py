from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import User, error_messages

from .constants import (
    USERNAME_REQUIRED,
    USERNAME_EXISTS,
    PASSWORD_REQUIRED,
    PASSWORD_TOO_SHORT,
    PASSWORD_MIN_LENGTH,
    EMAIL_REQUIRED,
    EMAIL_EXISTS,
)


def authenticated_user(data):
    '''Authentication process.'''

    username = data.get('username', None)
    password = data.get('password', None)

    if username is None:
        raise serializers.ValidationError(
            'A username is required to log in.'
        )

    if password is None:
        raise serializers.ValidationError(
            'A password is required to log in.'
        )

    user = authenticate(username=username, password=password)

    if user is None:
        raise serializers.ValidationError(
            'A user with this username and password was not found.'
        )

    if not user.is_active:
        raise serializers.ValidationError(
            'This user has been deactivated.'
        )

    return user


class SignupSerializer(serializers.ModelSerializer):
    '''Requests and creates a new user.'''

    id = serializers.SerializerMethodField(read_only=True)

    def get_id(self, obj):
        return obj.pk

    is_admin = serializers.SerializerMethodField(read_only=True)

    def get_is_admin(self, obj):
        return obj.is_staff

    password = serializers.CharField(
        write_only=True,
        error_messages=error_messages['password']['error_messages']
    )

    token = serializers.CharField(read_only=True)

    class Meta:
        model = User

        # Fields possibly included in request or response
        fields = ['id', 'username', 'password', 'email', 'is_admin', 'token']

        extra_kwargs = error_messages

    def create(self, validated_data):

        return User.objects.create_user(**validated_data)


class SigninSerializer(serializers.Serializer):
    '''Authenticates a user & creates a token.'''
    
    id = serializers.IntegerField(read_only=True)

    username = serializers.CharField(
        error_messages=error_messages['username']['error_messages']
    )

    password = serializers.CharField(
        write_only=True,
        error_messages=error_messages['password']['error_messages']
    )

    email = serializers.CharField(read_only=True)

    is_admin = serializers.BooleanField(read_only=True)

    token = serializers.CharField(read_only=True)

    def validate(self, data):
        user = authenticated_user(data)

        return {
            'id': user.pk,
            'username': user.username,
            'email': user.email,
            'is_admin': user.is_staff,
            'token': user.token
        }
