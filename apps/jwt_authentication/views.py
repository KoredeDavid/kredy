import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from rest_framework import generics, exceptions
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from apps.jwt_authentication.tokens import generate_access_token

UserModel = get_user_model()


class RefreshTokenAPIView(generics.GenericAPIView):

    @method_decorator(csrf_protect)
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token is None:
            raise exceptions.AuthenticationFailed(
                'Authentication credentials were not provided.')
        try:
            payload = jwt.decode(
                refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed(
                'expired refresh token, please login again.')

        user = UserModel.objects.get(id=payload.get('user_id'))
        if user is None:
            raise exceptions.AuthenticationFailed('UserModel not found')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('user is inactive')

        data = {
            'username': user.username,
            'email': user.email,
            'uuid': user.uuid,
            'is_verified': user.is_verified,
            'access_token': generate_access_token(user)
        }

        return Response(data, status=HTTP_201_CREATED)
