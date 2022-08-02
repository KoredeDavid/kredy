import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.account.validators import username_regex_validator, username_min_length
from apps.jwt_authentication import tokens
from my_blog.models_manger import MyModelManager


# Create your models here.


class CustomUser(AbstractUser):
    objects = MyModelManager('username', 'email')

    clean_method_is_called = False

    EMAIL = 'EL'
    GOOGLE = 'GE'

    AUTH_PROVIDER_CHOICES = [
        (EMAIL, 'Email'),
        (GOOGLE, 'Google'),
    ]

    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    auth_provider = models.CharField(max_length=2, choices=AUTH_PROVIDER_CHOICES, default=EMAIL)
    username = models.CharField(
        'username',
        max_length=30,
        help_text='Letters, digits and underscore only.',
        unique=True,
        validators=[username_regex_validator, username_min_length],
    )
    email = models.EmailField(
        'email address',
        unique=True,
        max_length=100,
        error_messages={'unique': 'A user with this email already exists'}
    )
    is_verified = models.BooleanField(default=False)

    def generate_tokens(self):
        return tokens.generate_tokens(self)

    def clean(self):
        self.clean_method_is_called = True

        if self.email is not None:
            self.email = self.email.lower()

    def save(self, *args, **kwargs):
        if not self.clean_method_is_called:
            self.full_clean()
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
