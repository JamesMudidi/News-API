import jwt
from datetime import datetime, timedelta
from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from core.managers import CustomQuerySet


class UserManager(BaseUserManager):
    # We are overiding the `create_user` method so that users can
    # only be created when all non-nullable fields are populated.

    def create_user(
        self,
        user_name=None,
        email=None,
        password=None,
    ):
        # Create and return a `User` with a phone number, first name, last name and
        # password.

        if not user_name:
            raise TypeError('Please provide your User name.')

        if not email:
            raise TypeError('Please provide your Phone number')

        if not password:
            raise TypeError('Please secure your account with a password')

        user = self.model(
            email=email, user_name=user_name
        )

        user.set_password(password)
        user.is_verified = True
        user.save()
        return user

    def create_superuser(
            self,
            user_name=None,
            email=None,
            password=None):
        # Create a superuser
        if not email:
            raise TypeError('Superusers must have an email.')

        if not password:
            raise TypeError('Superusers must have a password.')

        user = self.model(
            user_name=user_name, email=email)

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser):
    # Custom user model

    email = models.EmailField(max_length=16, unique=True)
    user_name = models.CharField(
        max_length=100, null=True, blank=True, unique=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
    active_objects = CustomQuerySet.as_manager()

    def __str__(self):
        return f'{self.email}'

    @property
    def get_email(self):
        # This method is required by Django for handling phone numbers.
        # Typically, this would be the user's first and last name. Since we do
        # not store the user's real name, we return their email instead.
        return self.email

    @property
    def token(self):
        # We need to make the method for creating our token private. At the
        # same time, it's more convenient for us to access our token with
        # `user.token` and so we make the token a dynamic property by wrapping
        # in in the `@property` decorator.
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """We generate JWT token and add the user id, email,
        user_name and expiration as an integer.
        """
        token_expiry = datetime.now() + timedelta(hours=24)
        token = jwt.encode({
            'id': self.pk,
            'email': self.email,
            'user_name': self.user_name,
            'exp': token_expiry.utcfromtimestamp(token_expiry.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')
