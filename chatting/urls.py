from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('chat_new/', new_message, name='chat_new'),
    path('chat_detail/<int:id>/', detail_message, name='chat_detail'),
    path('chat_received', receive_message, name='chat_received'),
    path('chat_send', send_message, name='chat_send'),
]