# live_chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer 


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']  
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)( 
            self.room_group_name, 
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        name = text_data_json['name']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'name': name
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        name = event['name']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'name': name
        }))

# live_chat/consumers.py
# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from .models import ChatMessage, ChatRoom
# from .serializers import ChatMessageSerializer

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = f"chat_{self.room_name}"

#         # Join the room group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave the room group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         # Create and save the chat message
#         room = ChatRoom.objects.get(room_name=self.room_name)
#         chat_message = ChatMessage(message=message, user=self.scope['user'], room=room)
#         chat_message.save()

#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat.message',
#                 'message': message,
#                 'username': self.scope['user'].username
#             }
#         )

#     async def chat_message(self, event):
#         message = event['message']
#         username = event['username']

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message,
#             'username': username
#         }))


# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from .models import ChatRoom, ChatMessage
# from asgiref.sync import async_to_sync, sync_to_async

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = f"chat_{self.room_name}"

#         # Join the room group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave the room group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#         username = self.scope["user"].username

#         await self.save_message(username, message)

#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat.message',
#                 'message': message,
#                 'username': username
#             }
#         )

#     async def chat_message(self, event):
#         message = event['message']
#         username = event['username']

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message,
#             'username': username
#         }))

#     @sync_to_async
#     def save_message(self, username, message):
#         room = ChatRoom.objects.get(room_name=self.room_name)
#         ChatMessage.objects.create(room=room, 
#                                 #    user=self.scope["user"], 
#                                    user = self.scope["user"]._wrapped,
#                                    message=message)

# import json
# from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
# from asgiref.sync import async_to_sync

# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_group_name = 'test'

#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )

#         self.accept()
   

#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type':'chat_message',
#                 'message':message
#             }
#         )
#         print(message)

#     def chat_message(self, event):
#         message = event['message']

#         self.send(text_data=json.dumps({
#             'type':'chat',
#             'message':message
#         })) 

#         print(message)


# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # Get the chat room name from the URL
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = f"chat_{self.room_name}"

#         # Join the chat room
#         await self.channel_layer.group_add( 
#             self.room_group_name,
#             self.channel_name
#         )

#         # Accept the WebSocket connection
#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave the chat room
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         # Receive a message from the WebSocket
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         # Send the message to the chat room group
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat.message',
#                 'message': message
#             }
#         )

#     async def chat_message(self, event):
#         # Send a message to the WebSocket
#         message = event['message']

#         # Send the message to the connected WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message
#         }))

