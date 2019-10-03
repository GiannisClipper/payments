from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin

from django.core.validators import MinLengthValidator

from datetime import datetime

import jwt  # pip install pyjwt

from apps.settings import SECRET_KEY, JWTOKEN_PREFIX, JWTOKEN_DURATION

from .constants import (
    USERNAME_REQUIRED,
    USERNAME_EXISTS,
    PASSWORD_REQUIRED,
    PASSWORD_TOO_SHORT,
    PASSWORD_MIN_LENGTH,
    EMAIL_REQUIRED,
    EMAIL_EXISTS,

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

    def create_user(self, username=None, email=None, password=None):
        '''Creates and returns a user.'''

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            password=password
        )

#        if not password or not password.strip():
#            user.password = None  # Should raise a required message
#        else:
#            user.set_password(password)  # Should store as hashed string

        # Remove leading or trailing spaces from strings
        for field in user._meta.fields:
            if isinstance(field, (models.CharField, models.TextField)):
                value = getattr(user, field.name)
                if value:
                    setattr(user, field.name, value.strip())

        user.full_clean()  # Field validations run here
        user.set_password(user.password)  # Stored as hashed string
        user.save()

        return user

    def create_superuser(self, username, email, password):
        '''Creates and returns a user with superuser permissions.'''

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    '''Defines a custom user model.'''

    username = models.CharField(
        max_length=128,
        db_index=True,
        unique=True,
        null=False,
        blank=False
    )

    password = models.CharField(
        max_length=128,
        validators=[MinLengthValidator(PASSWORD_MIN_LENGTH)],
        null=False,
        blank=False
    )

    email = models.EmailField(
        max_length=128,
        db_index=True,
        unique=True,
        null=False,
        blank=False
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'  # Which field is used to signin
    # REQUIRED_FIELDS = ['email']  # ['username']

    objects = UserManager()

    def __init__(self, *args, **kwargs):
        super(AbstractBaseUser, self).__init__(*args, **kwargs)
        super(PermissionsMixin, self).__init__(*args, **kwargs)

        # `error_messages` are used when `full_clean()` method is called
        # before `save()` method and database constraints
        field = self._meta.get_field('username')
        field.error_messages['required'] = USERNAME_REQUIRED
        field.error_messages['null'] = USERNAME_REQUIRED
        field.error_messages['blank'] = USERNAME_REQUIRED
        field.error_messages['unique'] = USERNAME_EXISTS

        field = self._meta.get_field('password')
        field.error_messages['required'] = PASSWORD_REQUIRED
        field.error_messages['null'] = PASSWORD_REQUIRED
        field.error_messages['blank'] = PASSWORD_REQUIRED
        field.error_messages['min_length'] = PASSWORD_TOO_SHORT

        field = self._meta.get_field('email')
        field.error_messages['required'] = EMAIL_REQUIRED
        field.error_messages['null'] = EMAIL_REQUIRED
        field.error_messages['blank'] = EMAIL_REQUIRED
        field.error_messages['unique'] = EMAIL_EXISTS

#    def clean(self):
#        for field in self._meta.fields:
#            if isinstance(field, (models.CharField, models.TextField)):
#                value = getattr(self, field.name)
#                if value:
#                    setattr(self, field.name, value.strip())

    def update(self, **fields):
        '''Updates and returns a user.'''

        for key, value in fields.items():
            setattr(self, key, value)

        for field in self._meta.fields:
            if isinstance(field, (models.CharField, models.TextField)):
                value = getattr(self, field.name)
                if value:
                    setattr(self, field.name, value.strip())

        self.full_clean()  # Field validations run here

        if 'password' in fields.keys():
            self.set_password(self.password)  # Stored as hashed string

        self.save()

        return self

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
