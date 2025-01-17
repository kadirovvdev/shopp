from django.urls import re_path
from . import chat_consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', chat_consumers.ChatConsumer.as_asgi()),
]
