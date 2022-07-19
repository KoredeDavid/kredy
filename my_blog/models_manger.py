from django.db import models


class MyModelManager(models.Manager):
    """
    This class ensures the *fields are case insensitive for unique validation.
    i.e 'KoredE' and 'korede' will be seen as the same values
    """
    def __init__(self, *fields):
        self.fields = fields
        super().__init__()

    def filter(self, **kwargs):
        for field in self.fields:
            if field in kwargs:
                kwargs[f'{field}__iexact'] = kwargs[field]
                del kwargs[field]            
            
        return super().filter(**kwargs)

    def get(self, **kwargs):
        for field in self.fields:
            if field in kwargs:
                kwargs[f'{field}__iexact'] = kwargs[field]
                del kwargs[field]            
            
        return super().get(**kwargs)
