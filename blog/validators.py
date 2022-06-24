from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinLengthValidator, RegexValidator

from . import models


username_validator = RegexValidator(regex=r'^[\w]+\Z', message=_('Enter a valid username. This value may contain only '
                                                                 'letters, numbers and underscore.'), flags=0, )
username_min_length = MinLengthValidator(5)


def author_validation(value):
    user = models.CustomUser.objects.get(id=value)
    if not user.is_author:
        raise ValidationError('The user must be an author')


def approved_by_validation(value):
    user = models.CustomUser.objects.get(id=value)
    if not user.is_boss:
        raise ValidationError('Posts can only be approved by bosses')
