from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, RegexValidator

from . import models

username_regex_validator = RegexValidator(regex=r'^[\w]+\Z', message='Enter a valid username. This value may contain only '
                                                               'letters, numbers and underscore.', flags=0, )
username_min_length = MinLengthValidator(5)

