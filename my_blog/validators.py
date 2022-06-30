from django.core.exceptions import ValidationError


def case_insensitive_unique_validator(instance, field):
    """
    Django's unique field validator, meaning it sees 'Korede' and 'korede' as two diff values
    This simple validator helps solve that problem
    """
    same_object = instance is field

    assert same_object, "The Instance and field value should be of same class object"

    field_query = {f'{field}__iexact': field}

    try:
        query_value = instance.objects.get(**field_query)
    except instance.DoesNotExist:
        query_value = None

    if query_value:
        if query_value.id != instance.id:
            raise ValidationError({f'{field}': f"This {field} already exists"})
