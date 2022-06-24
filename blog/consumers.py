# It allows for async code


import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from blog.models import Post


class PostConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected", event)

        await self.send({
            "type": "websocket.accept"
        })

        from_url = self.scope['url_route']['kwargs']['username']
        authenticated_user = self.scope['user']
        print(from_url, authenticated_user)
        # post_author = await self.get_author(authenticated_user)

        await self.send({
            "type": 'websocket.send',
            "text": "Sup Sup Internet"
        })

    async def websocket_receive(self, event):
        print("receive", event)
        # {'type': 'websocket.receive', 'text': '{"body":"qwertyuiop"}'}

        # This na string
        front_text = event.get('text', None)
        if front_text:
            # This na dict
            loaded_data = json.loads(front_text)
            loaded_data = loaded_data.get('body')
            await self.send({
                "type": 'websocket.send',
                "text": f"The shit the form sent to server and the server dey send back to the client na {loaded_data} "
            })

    async def websocket_disconnect(self, event):
        print("disconnected", event)

    @database_sync_to_async
    def get_author(self, user):
        return Post.objects.filter(author=user).values_list('author', flat=True)[0]
