# chat/urls.py

from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('chat/index/', index, name='index'),
    path('chat/room/', room, name='room'),
]
