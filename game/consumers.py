# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import threading

class TicTacToeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = 'room_%s' % self.room_name
        print("connected",self.room_name)
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        response = json.loads(text_data)
        event = response.get("event", None)
        message = response.get("message", None)
        print(threading.get_native_id(),event,message)
        # Send message to room group
        if event == 'MOVE':
            # Send message to room group
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'chat_message',
                'message': message,
                "event": "MOVE"
            })
        if event == 'START':
            # Send message to room group
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'chat_message',
                'message': message,
                'event': "START"
            })
        if event == 'END':
            # Send message to room group
            await self.channel_layer.group_send(self.room_group_name, {
                'type': 'chat_message',
                'message': message,
                'event': "END"
            })

    # Receive message from room group
    async def chat_message(self, event):
        # message = event['message']
        print("message",threading.get_native_id())
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'payload': event
        }))