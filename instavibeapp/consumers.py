from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.template.loader import render_to_string
from django.utils.timezone import localtime
from .models import Notification
from datetime import datetime

import logging

logger = logging.getLogger(__name__)

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.info(f"{self.scope['user']} connected to WebSocket {self.group_name}")

        if self.scope["user"].is_anonymous:
            logger.warning("Anonymous user tried to connect, closing")
            await self.close()
            return

        self.user = self.scope["user"]
        self.group_name = f"user_{self.user.id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        logger.info(f"{self.user} connected to WebSocket {self.group_name}")
        await self.accept()


    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_notification(self, event):
        logger.info(f"At Consumer lEVEL: Received event in consumer: {event}")
        type = event["data"]["type"]
        if type == "like":
            message = f"{event['data']['sender']} liked your post."
        elif type == "comment":
            message = f"{event['data']['sender']} commented on your post."
        elif type == "follow":
            message = f"{event['data']['sender']} started following you."
        timestamp = localtime(datetime.fromisoformat(event["data"]["created_at"]))
        logger.info(f"Prepared message at Consumer: {message} at {timestamp}")
        html = render_to_string("partials/notification-items.html", {
            "notification": {
                "message": message,
                "timestamp": timestamp
            }
        })
        
        await self.send(text_data=html)
        logger.info("Sent HTML to WebSocket")

