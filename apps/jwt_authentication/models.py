import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.


class AuthenticationToken(models.Model):
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                             related_name='user_token')
    token = models.CharField(max_length=255, unique=True)
    blacklist = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}'
