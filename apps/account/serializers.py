from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.forms import ValidationError
from django.template.loader import render_to_string
from django.urls import reverse
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator
from rest_framework import exceptions

from apps.jwt_authentication import tokens
from apps.jwt_authentication.serializers import AuthTokenSerializer

UserModel = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(validators=[validate_password], write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        # validator_queryset = UserModel.objects.all().values_list('username')
        # username_validator_message = "User with this username already exists"

        model = UserModel
        fields = ('username', 'email', 'auth_provider', 'password', 'password2')

        extra_kwargs = {
            'uuid': {
                'read_only': True
            },
            # 'username': {
            #     'validators': [
            #         UniqueValidator(queryset=validator_queryset,
            #                         message=username_validator_message, lookup='iexact'),
            #     ]
            # },
        }

    def validate(self, attrs):
        password1 = attrs.get("password")
        password2 = attrs.get("password2")
        if password1 and password2 and password1 != password2:
            raise serializers.ValidationError({"password2": "Passwords don't match"})

        return attrs

    def save(self, request, **kwargs):
        del self.validated_data['password2']

        try:
            user = super().save(**kwargs)
        except ValidationError as error_message:
            raise exceptions.ValidationError(error_message.error_dict)

        token = tokens.generate_access_token(user, days=3)
        protocol = request.scheme,
        domain = get_current_site(request).domain
        relative_link = reverse('verify-email')
        context = {
            #   protocol://domain/relative_link.com?token=<token>
            'activate_account_url': f"{protocol[0]}://{domain}{relative_link}?token={token}",
            'user': user,
        }

        email_subject = "K: Verification link!!!"
        email_body = render_to_string('account/activation_email.txt', context)
        email = EmailMessage(subject=email_subject, body=email_body, to=[user.email])
        email.send()

        del self.validated_data['password']
        data = {
            **self.validated_data,
            'uuid': user.uuid,
            'is_verified': user.is_verified,
            'tokens': user.generate_tokens()
        }

        return data


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    tokens = AuthTokenSerializer(read_only=True)

    class Meta:
        model = UserModel
        fields = ('username', 'password', 'email', 'auth_provider', 'is_verified', 'uuid', 'tokens')
        extra_kwargs = {
            'uuid': {
                'read_only': True
            },
            'email': {
                'read_only': True
            },
            'is_verified': {
                'read_only': True
            }
        }

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            raise AuthenticationFailed('Your username or password is incorrect!!!')

        if not user.is_active:
            raise AuthenticationFailed(
                f'{user.username}, your account is not active. Please reach out to the site admin.')

        data = {
            'uuid': user.uuid,
            'username': user.username,
            'email': user.email,
            'auth_provider': user.auth_provider,
            'is_verified': user.is_verified,
            'tokens': user.generate_tokens()
        }

        return data
