from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from apps.jwt_authentication.serializers import AuthTokenSerializer

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(validators=[validate_password], write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = ('username', 'email', 'uuid', 'password1', 'password2')

        extra_kwargs = {
            'uuid': {
                'read_only': True
            }
        }

    def validate(self, attrs):
        password1 = attrs.get("password1")
        password2 = attrs.get("password2")
        if password1 and password2 and password1 != password2:
            raise serializers.ValidationError({"password2": "Passwords don't match"})
        return attrs

    def save(self):
        user = UserModel(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
        )
        user.set_password(self.validated_data['password1'])
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(max_length=30)
    email = serializers.EmailField(read_only=True)
    uuid = serializers.UUIDField(read_only=True)
    tokens = AuthTokenSerializer(read_only=True)

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
            'tokens': user.get_tokens()
        }

        return data
