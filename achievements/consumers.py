# achievements/consumers.py
from channels.generic.websocket import AsyncJsonWebsocketConsumer

class NotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            print("⛔ Anónimo, cerrando WS")
            await self.close()
            return

        self.group_name = f"user_{self.scope['user'].id}"
        print("✅ WS conectado, grupo:", self.group_name)
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        print("🔌 WS desconectado")
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def achievement_unlocked(self, event):
        print("📨 Recibido evento en consumer:", event)
        await self.send_json(event["data"])