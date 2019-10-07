from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin

from django.core.validators import MinLengthValidator

from datetime import datetime

from .jwtokens.handlers import JWTokenHandler

from apps.settings import JWTOKEN_DURATION

from .constants import (
    USERNAME_REQUIRED,
    USERNAME_EXISTS,
    PASSWORD_REQUIRED,
    PASSWORD_TOO_SHORT,
    PASSWORD_MIN_LENGTH,
    EMAIL_REQUIRED,
    EMAIL_EXISTS,
)

error_messages = {
    'username': {
        'error_messages': {
            'required': USERNAME_REQUIRED,
            'null': USERNAME_REQUIRED,
            'blank': USERNAME_REQUIRED,
            'unique': USERNAME_EXISTS,
        }
    },
    'password': {
        'error_messages': {
            'required': PASSWORD_REQUIRED,
            'null': PASSWORD_REQUIRED,
            'blank': PASSWORD_REQUIRED,
            'min_length': PASSWORD_TOO_SHORT,
        }
    },
    'email': {
        'error_messages': {
            'required': EMAIL_REQUIRED,
            'null': EMAIL_REQUIRED,
            'blank': EMAIL_REQUIRED,
            'unique': EMAIL_EXISTS,
        }
    },
}


class UserManager(BaseUserManager):
    '''
    Custom `user` models must define their own manager class,
    inheriting from `BaseUserManager` get a lot of Django code.
    '''

    def create_user(self, username=None, email=None, password=None):
        '''Creates and returns a user.'''

        user = self.model(
            username=username,
            email=self.normalize_email(email)
        )

        # `password` value assigned after initializing `user` object in order
        # to be converted to hashed string by the customized `save` method
        user.password = password

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
        blank=False,
        error_messages=error_messages['username']['error_messages']
    )

    password = models.CharField(
        max_length=128,
        validators=[MinLengthValidator(PASSWORD_MIN_LENGTH)],
        null=False,
        blank=False,
        error_messages=error_messages['password']['error_messages']
    )

    email = models.EmailField(
        max_length=128,
        db_index=True,
        unique=True,
        null=False,
        blank=False,
        error_messages=error_messages['email']['error_messages']
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'  # Field is used to signin (ex. 'email')

    saved_password = None  # Helps to identify and hash new passwords

    objects = UserManager()

    def save(self, *args, **kwargs):

        # Remove leading or trailing spaces from strings
        for field in self._meta.fields:
            if isinstance(field, (models.CharField, models.TextField)):
                value = getattr(self, field.name)
                if value:
                    setattr(self, field.name, value.strip())

        # Field validations run here
        self.full_clean()

        # Only new passwords should be converted to hashed strings
        if self.saved_password != self.password:
            self.set_password(self.password)
            self.saved_password = self.password

        super().save(*args, **kwargs)

    def update(self, **fields):
        '''Updates and returns a user.'''

        for key, value in fields.items():
            setattr(self, key, value)

        self.save()

        return self

    def __str__(self):
        return self.username

    @property  # This decorator defines a dynamic property
    def token(self):
        '''Generates a JSON Web Token with user info and expiry time.'''

        now = datetime.timestamp(datetime.utcnow())
        expiration = now + JWTOKEN_DURATION
        key = JWTokenHandler.encode_key({
            'user_id': self.pk,
            'expiration': expiration
        })

        return key
