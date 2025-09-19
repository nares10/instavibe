from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.template.loader import render_to_string
from django.utils.timezone import localtime
from .models import Notification

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close()
            return

        self.user = self.scope["user"]
        self.group_name = f"user_{self.user.id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        # Send any unread notifications on connect
        unread = await self.get_unread()
        for n in unread:
            html = render_to_string("notifications.html", {
                "message": n.message,
                "timestamp": localtime(n.timestamp)
            })
            await self.send(text_data=html)
            await self.mark_read(n)

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_notification(self, event):
        type = event["data"]["type"]
        if type == "like":
            message = f"{event['data']['sender']} liked your post."
        elif type == "comment":
            message = f"{event['data']['sender']} commented on your post."
        elif type == "follow":
            message = f"{event['data']['sender']} started following you."
        timestamp = localtime(event["data"]["created_at"])
        html = render_to_string("notifications.html", {
            "message": message,
            "timestamp": timestamp
        })
        await self.send(text_data=html)

    @database_sync_to_async
    def get_unread(self):
        return list(Notification.objects.filter(user=self.user, is_read=False))

    @database_sync_to_async
    def mark_read(self, n):
        n.is_read = True
        n.save()
