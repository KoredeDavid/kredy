from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from apps.account.validators import username_regex_validator, username_min_length
from my_blog.validators import case_insensitive_unique_validator


# Create your models here.


class CustomUser(AbstractUser):
    clean_method_is_called = False

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
    email = models.EmailField('email address', blank=False, null=True, unique=True)

    def clean(self):
        self.clean_method_is_called = True

        if self.email is not None:
            self.email = self.email.lower()

        case_insensitive_unique_validator(self, self.username)

    def save(self, *args, **kwargs):
        if not self.clean_method_is_called:
            self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
