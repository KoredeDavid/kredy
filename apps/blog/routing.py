from django.urls import path
from apps.blog.consumers import PostConsumer

websocket_urlpatterns =[
    path('articles-factory/<username>/', PostConsumer.as_asgi()),
]


