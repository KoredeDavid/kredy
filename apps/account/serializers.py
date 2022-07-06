from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.validators import UniqueValidator

from apps.jwt_authentication import tokens
from apps.jwt_authentication.serializers import AuthTokenSerializer

UserModel = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(validators=[validate_password], write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        validator_queryset = UserModel.objects.all().values_list('email', 'username')
        email_validator_message = "A user with that email already exists"
        username_validator_message = "A user with that username already exists"

        model = UserModel
        fields = ('username', 'email', 'password1', 'password2')

        extra_kwargs = {
            'uuid': {
                'read_only': True
            },
            'username': {
                'validators': [
                    UniqueValidator(queryset=validator_queryset,
                                    message=username_validator_message, lookup='iexact'),
                ]
            },
            'email': {
                'validators': [
                    UniqueValidator(queryset=validator_queryset,
                                    message=email_validator_message, lookup='iexact'),
                ]
            }
        }

    def validate(self, attrs):
        password1 = attrs.get("password1")
        password2 = attrs.get("password2")
        if password1 and password2 and password1 != password2:
            raise serializers.ValidationError({"password2": "Passwords don't match"})

        return attrs

    def save(self, request, **kwargs):
        user = UserModel(
            username=self.validated_data['username'],
            email=self.validated_data['email'].lower(),
        )
        user.set_password(self.validated_data['password1'])
        user.clean_method_is_called = True
        user.save()

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

        self.validated_data.pop('password1')
        self.validated_data.pop('password2')

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
        fields = ('username', 'password', 'email', 'is_verified',  'uuid', 'tokens')
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
            'username': user.username,
            'email': user.email,
            'uuid': user.uuid,
            'is_verified': user.is_verified,
            'tokens': user.generate_tokens()
        }

        return data
