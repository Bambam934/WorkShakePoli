from channels.generic.websocket import AsyncJsonWebsocketConsumer

class NotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        if self.scope['user'].is_anonymous:
            return await self.close()
        self.group = f"user_{self.scope['user'].id}"
        await self.channel_layer.group_add(self.group, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group, self.channel_name)

    # Este método se invocará cuando enviemos el evento tipo "achievement.unlocked"
    async def achievement_unlocked(self, event):
        await self.send_json(event['data'])
