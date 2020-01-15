from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin

from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError

from .jwtokens.models import JWToken

from .constants import (
    USERNAME_REQUIRED,
    USERNAME_EXISTS,
    PASSWORD_REQUIRED,
    PASSWORD_TOO_SHORT,
    PASSWORD_MIN_LENGTH,
    PASSWORD_NOT_CONFIRMED,
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

    def create_user(self, username=None, email=None, password=None, password2=None):
        '''Creates and returns a user.'''

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        # `password` value assigned after initializing `user` object in order
        # to be converted to hashed string by the customized `save` method
        user.password = password
        user.password2 = password2

        user.save()

        return user

    def create_superuser(self, username=None, email=None, password=None, password2=None):
        '''Creates and returns a user with superuser permissions.'''

        user = self.create_user(username, email, password, password2)
        user.is_superuser = True
        user.is_staff = True

        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin, JWToken):
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

    hashed_password = None  # Helps to identify and hash new passwords
    password1 = None  # Help to password confirmation
    password2 = None  # Help to password confirmation

    objects = UserManager()

    # There are three steps involved in validating a model:
    # Validate the model fields - Model.clean_fields()
    # Validate the model as a whole - Model.clean()
    # Validate the field uniqueness - Model.validate_unique()
    # All three steps are performed when you call full_clean() method.

    def clean_fields(self, *args, **kwargs):
        # Remove leading or trailing spaces from strings
        for field in self._meta.fields:
            if isinstance(field, (models.CharField, models.TextField)):
                value = getattr(self, field.name)
                if value is not None:
                    setattr(self, field.name, value.strip())

        super().clean_fields(*args, **kwargs)

    def clean(self, *args, **kwargs):
        # Only new passwords should be confirmed
        if self.hashed_password != self.password != self.password2:
            raise ValidationError({'password2': PASSWORD_NOT_CONFIRMED})

        super(User, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Field validations run here
        self.full_clean()

        # Only new passwords should be converted to hashed strings
        if self.hashed_password != self.password:
            self.set_password(self.password)
            self.hashed_password = self.password

        super().save(*args, **kwargs)

    def update(self, **fields):
        '''Updates and returns a user.'''

        self.hashed_password = self.password

        for key, value in fields.items():
            setattr(self, key, value)

        self.save()

        return self

    def __str__(self):
        return self.username
