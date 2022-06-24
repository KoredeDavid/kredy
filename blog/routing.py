from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
from django.urls import path, re_path
from django.core.asgi import get_asgi_application
from blog.consumers import PostConsumer

websocket_urlpatterns =[
    path('articles-factory/<username>/', PostConsumer.as_asgi()),
]


