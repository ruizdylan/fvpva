from django.urls import re_path, path

from . import consumer
from .consumer import BoughtNumbersConsumer, MessageReceiverConsumer

websocket_urlpatterns = [

    # re_path(r'ws/socket-server/', consumer.ChatConsumer.as_asgi()),

    path('ws/bought-services/', BoughtNumbersConsumer.as_asgi()),

    path('ws/message-receiver/<int:id>', MessageReceiverConsumer.as_asgi()),

]