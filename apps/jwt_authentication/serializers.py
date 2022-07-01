from rest_framework import serializers

from apps.jwt_authentication.models import AuthenticationToken


class AuthTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthenticationToken
        exclude = ('user',)

