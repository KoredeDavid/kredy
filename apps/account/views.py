import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse
from rest_framework import generics, status
from rest_framework.response import Response

from apps.account.serializers import RegisterSerializer, LoginSerializer, EmailVerificationSerializer
from apps.jwt_authentication import tokens

UserModel = get_user_model()


class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    # renderer_classes = (UserRenderer,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(request=request)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VerifyEmailAPIView(generics.GenericAPIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        serializer = self.serializer_class()
        serializer.is_valid(raise_exception=True)
        serializer.save(request=request)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
