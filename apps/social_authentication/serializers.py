import os
from rest_framework import serializers
from .socials import google
from .register import register_or_login_social_user
from rest_framework.exceptions import AuthenticationFailed


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        self.user_data = google.Google.validate(auth_token)

        try:
            self.user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        if self.user_data['aud'] != os.environ.get('GOOGLE_CLIENT_ID'):
            raise AuthenticationFailed('oops, who are you?')

    def save(self):
        user_id = self.user_data['sub']
        email = self.user_data['email']
        name = self.user_data['name']
        provider = 'GE'

        return register_or_login_social_user(
            provider=provider, user_id=user_id, email=email, name=name)
