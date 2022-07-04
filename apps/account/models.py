import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.account.validators import username_regex_validator, username_min_length
from apps.jwt_authentication import tokens
from my_blog.validators import case_insensitive_unique_validator


# Create your models here.


class CustomUser(AbstractUser):
    clean_method_is_called = False

    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    username = models.CharField(
        'username',
        max_length=30,
        help_text='Letters, digits and underscore only.',
        unique=True,
        validators=[username_regex_validator, username_min_length],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    email = models.EmailField('email address', unique=True)
    is_verified = models.BooleanField(default=False)

    def generate_tokens(self):
        return tokens.generate_tokens(self)

    def get_tokens(self):
        return tokens.get_tokens(self)

    def clean(self):
        self.clean_method_is_called = True

        if self.email is not None:
            self.email = self.email.lower()

        id_ = None
        if self.id:
            id_ = self.id

        case_insensitive_unique_validator(self, "username", self.username, id_)

    def save(self, *args, **kwargs):
        if not self.clean_method_is_called:
            self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
