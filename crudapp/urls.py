from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('new/', new, name='new'),
    path('detail/<int:id>/', detail, name='detail'),
    path('edit/<str:id>', edit, name="edit"),
    path('delete/<str:id>', delete, name="delete"),
    path('search', search, name='search'),
    path('mail/', email, name='mail'),
]