# views.py

from django.shortcuts import render
from django.http import JsonResponse
from .models import Message

def chat_room(request, room_name):
    return render(request, 'chat/chat_room.html', {'room_name': room_name})

def get_messages(request, room_name):
    messages = Message.objects.filter(room_name=room_name).order_by('timestamp')
    return JsonResponse([{'content': msg.content, 'timestamp': msg.timestamp} for msg in messages], safe=False)
