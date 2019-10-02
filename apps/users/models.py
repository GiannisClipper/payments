from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin

from datetime import datetime

import jwt  # pip install pyjwt

from apps.settings import SECRET_KEY, JWTOKEN_PREFIX, JWTOKEN_DURATION

from .constants import (
    USERNAME_REQUIRED,
    USERNAME_EXISTS,
    EMAIL_REQUIRED,
    EMAIL_EXISTS,
    PASSWORD_REQUIRED,
    TOKEN_KEY_NOT_VALID,
    TOKEN_USER_NOT_EXISTS,
    TOKEN_USER_NOT_ACTIVE,
    TOKEN_KEY_EXPIRED,
    TOKEN_HEADER_NOT_VALID,
    TOKEN_HEADER_PREFIX_NOT_VALID,
)


class UserManager(BaseUserManager):
    '''
    Custom `user` models must define their own manager class,
    inheriting from `BaseUserManager` get a lot of Django code.
    '''

    def create_user(self, username, email, password=None):
        '''Creates and returns a user.'''

        errors = []
        if not username:
            errors += [USERNAME_REQUIRED]

        elif self.model.objects.filter(username=username):
            errors += [USERNAME_EXISTS]

        if not email:
            errors += [EMAIL_REQUIRED]

        elif self.model.objects.filter(email=email):
            errors += [EMAIL_EXISTS]

        if errors:
            raise Exception(','.join(errors))

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        '''Creates and returns a user with superuser permissions.'''

        if not password:
            raise TypeError(PASSWORD_REQUIRED)

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    '''Defines a custom user model.'''

    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    # I've tried: error_messages={'unique': EMAIL_EXISTS})
    # but couldn't override the `unique constraint` db error

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # USERNAME_FIELD define which field is used to signin
    USERNAME_FIELD = 'username'  # ''email'
    REQUIRED_FIELDS = ['email']  # ['username']

    objects = UserManager()

    def __str__(self):
        return self.username

    @property  # This decorator defines a dynamic property
    def token(self):
        '''Generates a JSON Web Token with user info and expiry time.'''

        now = datetime.timestamp(datetime.utcnow())
        expiration = now + JWTOKEN_DURATION
        key = JWTokenHandler.encode_key(self.pk, expiration)

        return key


class JWTokenHandler():

    def compose_header(key):
        '''Composes a JSON Web Token header with prefix and key.'''

        header = JWTOKEN_PREFIX + ' ' + key
        return header

    def decompose_header(header):
        '''Decomposes a valid JSON Web Token header and returns the key.'''

        header = header.split()

        if not header or len(header) != 2:
            raise Exception(TOKEN_HEADER_NOT_VALID)

        # header[0] = header[0].decode('utf-8')
        # header[1] = header[1].decode('utf-8')

        if header[0] != JWTOKEN_PREFIX:
            raise Exception(TOKEN_HEADER_PREFIX_NOT_VALID)

        return header[1]

    def encode_key(payload):
        '''Generates a JSON Web Token with user info and expiry time.'''

        key = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return key.decode('utf-8')

    def decode_key(key):
        '''Decodes from a JSON Web Token user info and expiry time.'''

        try:
            payload = jwt.decode(key, SECRET_KEY)
        except Exception as err:
            raise Exception(TOKEN_KEY_NOT_VALID + ' ' + str(err))

        return payload

    def check_key_if_user_exists(id):
        '''Checks if the user's id in token exists in database.'''

        user = User.objects.get(pk=id)

        if not user:
            raise Exception(TOKEN_USER_NOT_EXISTS)

        return user

    def check_key_if_user_is_active(user):
        '''Checks if the user in token is active.'''

        if not user.is_active:
            raise Exception(TOKEN_USER_NOT_ACTIVE)

        return user

    def check_key_expiration(expiration):
        '''Checks if the token is expired.'''

        now = datetime.timestamp(datetime.utcnow())

        if expiration <= now:
            raise Exception(TOKEN_KEY_EXPIRED)

        return expiration
