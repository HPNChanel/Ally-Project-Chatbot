
#* Message Handling
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
  async def connect(self):
    #* Connect WebSocket
    self.room_name = f"user_{self.scope['user'].id}"
    self.room_group_name = f"chat_{self.room_name}"
    
    #* Attend to group
    await self.channel_layer.group_add(
      self.room_group_name,
      self.channel_layer
    )
    
    await self.accept()
  
  #* Disconnect group
  async def disconnect(self, close_code):
    await self.channel_layer.group_discard(
      self.room_group_name,
      self.channel_name
    )
  
  #* Receive message from WebSocket
  async def receive(self, text_data):
    data = json.loads(text_data)
    message = data.get("message")
    
    #* Send message to new group
    await self.channel_layer.group_send(
      self.room_group_name,
      {
        'type': 'chat_message',
        'message': message,
      }
    )
  
  #* Send message to WebSocket
  async def chat_message(self, event):
    message = event['message']
    
    await self.send(text_data=json.dumps({
      'message': message
    }))