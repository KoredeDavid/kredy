from django.contrib.auth import get_user_model, authenticate
import os
import random
from rest_framework.exceptions import AuthenticationFailed

UserModel = get_user_model()


def generate_username(name):
    username = "".join(name.split(' ')).lower()
    if not UserModel.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)


def register_or_login_social_user(provider, user_id, email, name):
    user = UserModel.objects.filter(email=email)

    if user.exists():
        user = user[0]

        if user.auth_provider == provider and user.is_verified:
            pass
        else:
            if user.auth_provider != provider:
                user.auth_provider = provider

            if not user.is_verified:
                user.is_verified = True

            user.save()

        return {
            'uuid': user.uuid,
            'username': user.username,
            'email': user.email,
            'auth_provider': user.auth_provider,
            'is_verified': user.is_verified,
            'tokens': user.generate_tokens()
        }
    else:
        user = {
            'username': generate_username(name),
            'email': email,
        }
        user = UserModel(**user)
        user.set_password(os.environ.get('SOCIAL_SECRET_PASSWORD'))
        user.is_verified = True
        user.auth_provider = provider
        user.save()

        return {
            'uuid': user.uuid,
            'username': user.username,
            'email': user.email,
            'auth_provider': user.auth_provider,
            'is_verified': user.is_verified,
            'tokens': user.generate_tokens()
        }
