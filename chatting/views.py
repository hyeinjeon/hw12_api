from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import message
from .models import Message
from .views import *
from .forms import MessageForm
from django.utils import timezone

# Create your views here.

def receive_message(request):
    chats = Message.objects.filter( receiver = request.user ) #DB에서 내가 받은것만 필터링
    return render(request, "chat_received.html", {'chats':chats})

def send_message(request):
    chats = Message.objects.filter( sender = request.user ) # 내가 보낸 것만 필터링
    return render(request, "chat_send.html", {'chats': chats})

def detail_message(request, id):
    chat = get_object_or_404(Message, pk = id)
    return render(request, 'chat_detail.html', {'chat': chat})

def new_message(request):
    if request.method == 'POST':
        chatform = MessageForm(request.POST, request.FILES)
        if chatform.is_valid():
            chat = chatform.save(commit=False)
            chat.pub_date = timezone.now()
            chat.save()
            return redirect('chat_detail', chat.id)
        return redirect('chat_send') #실패하면 내가 보낸 메세지함으로 가게
    else:
        chatform = MessageForm()
        return render(request, 'chat_new.html', {'chatform':chatform})