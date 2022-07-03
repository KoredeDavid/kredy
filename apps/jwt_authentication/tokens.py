from datetime import datetime, timedelta
import jwt
from django.conf import settings

from apps.jwt_authentication.models import AuthenticationToken


def generate_access_token(user, days=0, minutes=5):
    access_token_payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(days=days, minutes=minutes),
        'iat': datetime.utcnow()
    }

    access_token = jwt.encode(access_token_payload, settings.SECRET_KEY, algorithm='HS256')

    return access_token


def generate_refresh_token(user, days=60, minutes=0):
    refresh_token_payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(days=days, minutes=minutes),
        'iat': datetime.utcnow()
    }

    refresh_token = jwt.encode(refresh_token_payload, settings.SECRET_KEY, algorithm='HS256')

    return refresh_token


def generate_tokens(user):
    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)

    tokens = {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }

    try:
        user_token = AuthenticationToken.objects.get(user=user)
        user_token.access_token = access_token
        user_token.refresh_token = refresh_token
        user_token.save()
    except AuthenticationToken.DoesNotExist:
        user = {'user': user}
        data = {**user, **tokens}
        AuthenticationToken.objects.create(**data)

    return tokens


def get_tokens(user):
    user_token = AuthenticationToken.objects.get(user=user)

    tokens = {
        "access_token": user_token.access_token,
        "refresh_token": user_token.refresh_token,
    }

    return tokens
