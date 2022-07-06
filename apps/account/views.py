import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import generics, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from apps.account.serializers import RegisterSerializer, LoginSerializer

UserModel = get_user_model()


class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    # renderer_classes = (UserRenderer,)

    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save(request=request)

        response = Response(data, status=status.HTTP_201_CREATED)
        response.set_cookie(key='refresh_token', value=data['tokens']['refresh_token'], httponly=True)
        return response


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        response.set_cookie(key='refresh_token', value=serializer.data['tokens']['refresh_token'], httponly=True)
        return response


class VerifyEmailAPIView(generics.GenericAPIView):
    def get(self, request):
        token = request.GET.get('token')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed({'token': 'Activation link has expired!!!'})
        except jwt.exceptions.DecodeError:
            raise AuthenticationFailed({'token': 'Activation link is invalid!!!'})

        user = UserModel.objects.get(id=payload['user_id'])

        data = {
            'username': user.username,
            'email': user.email,
            'is_verified': True,
            'uuid': user.uuid,
            'tokens': user.get_tokens()
        }

        if not user.is_verified:
            user.is_verified = True
            user.save()
            return Response(data, status=status.HTTP_202_ACCEPTED)

        return Response(data, status=status.HTTP_202_ACCEPTED)
