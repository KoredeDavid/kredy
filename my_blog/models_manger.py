from django.contrib.auth.models import BaseUserManager


class MyModelManager(BaseUserManager):
    """
    This class ensures the *fields are case insensitive for unique validation.
    i.e 'KoredE' and 'korede' will be seen as the same values
    """

    def __init__(self, *fields):
        self.fields = fields
        super().__init__()

    def filter(self, *args, **kwargs):
        for field in self.fields:
            if field in kwargs:
                kwargs[f'{field}__iexact'] = kwargs[field]
                del kwargs[field]

        return super().filter(*args, **kwargs)

    def get(self, *args, **kwargs):
        for field in self.fields:
            if field in kwargs:
                kwargs[f'{field}__iexact'] = kwargs[field]
                del kwargs[field]

        return super().get(*args, **kwargs)
