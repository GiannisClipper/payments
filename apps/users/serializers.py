from rest_framework import serializers
from django.contrib.auth import authenticate
from django.core.validators import MinLengthValidator

from .models import User, error_messages

from .constants import (
    PASSWORD_MIN_LENGTH,
    PASSWORD_TOO_SHORT,
    INPUT_NOT_MATCH,
)


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
        validators=[
            MinLengthValidator(
                PASSWORD_MIN_LENGTH, 
                message=PASSWORD_TOO_SHORT
            )
        ],
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
        user = authenticate(
            username=data['username'],
            password=data['password']
        )

        if user is None or not user.is_active:
            raise serializers.ValidationError(INPUT_NOT_MATCH)

        return {
            'id': user.pk,
            'username': user.username,
            'email': user.email,
            'is_admin': user.is_staff,
            'token': user.token
        }


class UserSerializer(serializers.HyperlinkedModelSerializer):
    '''Handles serialization and deserialization of User objects.'''
    
    id = serializers.SerializerMethodField(read_only=True)

    def get_id(self, obj): 
        return obj.pk

    admin = serializers.SerializerMethodField(read_only=True)

    def get_admin(self, obj): 
        return obj.is_staff

    password = serializers.CharField(
        max_length=128,
        min_length=4,
        write_only=True
    )

    url = serializers.HyperlinkedIdentityField(
        view_name='users:byid',
        lookup_field='id',
        read_only=True, 
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'admin', 'is_active', 'url',)

        # Alternative to read_only=True, prefered
        # cause don't want to specify anything else
        # read_only_fields = ('token',)

    def get(self, instance):
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance

    def delete(self):
        user = authenticate(
            username=initial_data['username'],
            password=initial_data['password']
        )

        if user is None or not user.is_active:
            raise serializers.ValidationError(INPUT_NOT_MATCH)

        user.delete()

        return None