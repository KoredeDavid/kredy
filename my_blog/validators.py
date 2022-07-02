from django.core.exceptions import ValidationError


def case_insensitive_unique_validator(instance, field, value, _id=None):
    """
    Django's unique field validator, meaning it sees 'Korede' and 'korede' as two diff values
    This simple validator helps solve that problem
    """
    instance = instance.__class__

    field_query = {f'{field}__iexact': value}

    try:
        query_value = instance.objects.get(**field_query)
    except instance.DoesNotExist:
        query_value = None

    if query_value:
        if query_value.id != _id:
            raise ValidationError({f'{field}': f"This {field} already exists"})
