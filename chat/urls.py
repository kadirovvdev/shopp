# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('chat/<str:room_name>/', views.chat_room, name='chat-room'),
    path('api/messages/<str:room_name>/', views.get_messages, name='get_messages'),
]