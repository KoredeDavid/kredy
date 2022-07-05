import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from apps.account.serializers import RegisterSerializer, LoginSerializer

UserModel = get_user_model()


class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    # renderer_classes = (UserRenderer,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.save(request=request)

        return Response(user_data, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


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
