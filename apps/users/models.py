from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin

# import jwt  # pip install pyjwt
# from datetime import datetime

from .constants import Msg


class UserManager(BaseUserManager):
    """
    Custom `user` models must define their own manager class,
    by inheriting from `BaseUserManager`, get a lot of Django code.
    """

    def create_user(self, username, email, password=None):
        """Create and return a user."""

        if not username:
            raise TypeError(Msg.USERNAME_REQUIRED)

        if not email:
            raise TypeError(Msg.EMAIL_REQUIRED)

        if self.model.objects.filter(username=username):
            raise ValueError(Msg.USERNAME_EXISTS)

        if self.model.objects.filter(email=email):
            raise ValueError(Msg.EMAIL_EXISTS)

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        """Create and return a user with superuser/admin permissions."""

        if not password:
            raise TypeError(Msg.PASSWORD_REQUIRED)

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model."""

    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    # I've tried: error_messages={'unique': Msg.EMAIL_EXISTS})
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
