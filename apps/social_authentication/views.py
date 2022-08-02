from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import GoogleSocialAuthSerializer


# Create your views here.

class GoogleSocialAuthView(GenericAPIView):
    serializer_class = GoogleSocialAuthSerializer

    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        """
        POST with "auth_token"
        Send an idtoken as from google to get user information
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()

        response = Response(data, status=status.HTTP_200_OK)
        refresh_token = data['tokens']['refresh_token']
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)
        return response

# class FacebookSocialAuthView(GenericAPIView):

#     serializer_class = FacebookSocialAuthSerializer

#     def post(self, request):
#         """
#         POST with "auth_token"
#         Send an access token as from facebook to get user information
#         """

#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         data = ((serializer.validated_data)['auth_token'])
#         return Response(data, status=status.HTTP_200_OK)


# class TwitterSocialAuthView(GenericAPIView):
#     serializer_class = TwitterAuthSerializer

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         return Response(serializer.validated_data, status=status.HTTP_200_OK)