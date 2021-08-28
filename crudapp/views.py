from django import http
from django.core import paginator
from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog
from .forms import BlogForm
from django.utils import timezone
from django.core.mail import send_mail
from datetime import date, datetime, timedelta

def email(request):
    if request.method == 'POST':
        name = request.POST.get('full-name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        data = {
            'name' : name,
            'email' : email,
            'subject' : subject,
            'message' : message
        }
        message = '''
        New message: {}
        
        From: {}
        '''.format(data['message'], data['email'])
        send_mail(data['subject'], message, '', ['hayleyjhi@naver.com'])
        
    return render(request, 'mail.html', {})


# Create your views here.

def home(request):
    blogs = Blog.objects
    return render(request, 'home.html', {'blogs':blogs})

def api(request):
    return render(request, 'api.html')

def detail(request, id):
    blog = get_object_or_404(Blog, pk = id)
    response =  render(request, 'detail.html', {'blog':blog})

    #조회수 기능 (쿠키 이용)
    expire_date, now = datetime.now(), datetime.now()
    expire_date += timedelta(days=1)
    expire_date = expire_date.replace(hour=0, minute=0, second=0, microsecond=0)
    expire_date -= now
    max_age = expire_date.total_seconds()

    cookie_value = request.COOKIES.get('hitblog', '_')

    if f'_{id}_' not in cookie_value:
        cookie_value += f'{id}_'
        response.set_cookie('hitblog', value=cookie_value, max_age=max_age, httponly=True)
        blog.hits += 1
        blog.save()
    return response

def new(request):
    if request.method == 'POST': #글을 작성한 후 저장 버튼을 눌렀을 때
        post_form = BlogForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit = False)
            post.pub_date = timezone.now()
            post.save()
            return redirect('home')
    else:   #글을 쓰려고 들어갔을 때
        post_form = BlogForm()   #글을 입력받기 위한 빈 form을 불러옴
        return render(request, 'new.html', {'post_form':post_form})

def edit(request, id):
    post = get_object_or_404(Blog, pk = id)
    if request.method == 'GET': #수정하려고 들어갔을 때
        post_form = BlogForm(instance = post)
        #현재 post가 포함된 form을 불러옴
        return render(request, 'edit.html', {'edit_post':post_form})
    else:
        post_form = BlogForm(request.POST, request.FILES, instance = post)
        #현재 post에 가져온 정보를 form에 담음
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.pub_date = timezone.now()
            post.save()
        return redirect('/crudapp/detail/'+str(id))

def delete(request, id):
    delete_blog = Blog.objects.get(id = id)
    delete_blog.delete()
    return redirect('home')

def search(request):
    blogs = Blog.objects.all().order_by('-id')

    q = request.POST.get('q', "") 

    if q:
        blogs = blogs.filter(title__icontains=q)
        return render(request, 'search.html', {'blogs' : blogs, 'q' : q})
    
    else:
        return render(request, 'search.html')

