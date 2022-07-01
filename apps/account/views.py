from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response

from apps.account.serializers import UserSerializer, LoginSerializer

UserModel = get_user_model()


class UserAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    lookup_field = 'uuid'
    queryset = UserModel


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
