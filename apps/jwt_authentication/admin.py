from django.contrib import admin
from apps.jwt_authentication.models import AuthenticationToken

admin.site.register(AuthenticationToken)
