import json

from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

from api.order.models import Order
from api.services.models import ServiceNumber
from api.services.serializer import ServicesNumberHomeSerializer


class BoughtNumbersConsumer(AsyncWebsocketConsumer):
    async def websocket_connect(self, message):
        self.group_name = 'bought_numbers'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        # await self.send(text_data=json.dumps(message))

    # async def websocket_disconnect(self, message):
    #     await self.channel_layer.group_discard(
    #         self.group_name,
    #         self.channel_name
    #     )

    async def notify_clients(self, event):
        print("Data Sent")
        message = event['message']
        await self.send(text_data=json.dumps(message))

    async def websocket_receive(self, message):
        # You can handle additional commands or messages from the client here
        pass

    @staticmethod
    def get_latest_data():
        # This method retrieves the latest data from the database
        # You can modify it based on your database model
        latest_data = Order.objects.last()
        return latest_data.number_id

    @staticmethod
    def serialize_data(data):
        # This method serializes the data to send over the WebSocket
        number_instance = ServiceNumber(id=data)
        return ServicesNumberHomeSerializer(number_instance).data

    # def send_notification(self):

        # Use async_to_sync to call self.send() from a synchronous context
        # async_to_sync(self.send)(text_data=json.dumps(serialized_data))

    async def database_changes_notification(self, event):
        message = event['message']
        await self.send(text_data=message)


class MessageReceiverConsumer(AsyncWebsocketConsumer):
    async def websocket_connect(self, message):
        id = self.scope["url_route"]["kwargs"]["id"]
        self.group_name = f'message_receiver_{id}'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        # await self.send(text_data=json.dumps(message))

    # async def websocket_disconnect(self, message):
    #     await self.channel_layer.group_discard(
    #         self.group_name,
    #         self.channel_name
    #     )

    async def notify_clients(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))

    async def websocket_receive(self, message):
        # You can handle additional commands or messages from the client here
        pass

    @staticmethod
    def get_latest_data():
        # This method retrieves the latest data from the database
        # You can modify it based on your database model
        latest_data = Order.objects.last()
        return latest_data.number_id

    @staticmethod
    def serialize_data(data):
        # This method serializes the data to send over the WebSocket
        number_instance = ServiceNumber(id=data)
        return ServicesNumberHomeSerializer(number_instance).data

    # def send_notification(self):

        # Use async_to_sync to call self.send() from a synchronous context
        # async_to_sync(self.send)(text_data=json.dumps(serialized_data))

    async def database_changes_notification(self, event):
        message = event['message']
        await self.send(text_data=message)

# class ChatConsumer(WebsocketConsumer):
#
#     def connect(self):
#         self.accept()
#
#         self.send(text_data=json.dumps({
#             "type": "connection Established",
#             "message": "abc"
#         }))
#
#     def receive(self, text_data=None, bytes_data=None):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#         print(message)
