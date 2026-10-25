"""
Definition of views for Autoparts.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.forms import UserCreationForm  # ← ДОБАВИТЬ
from .models import Blog, Comment, Feedback
from .forms import CommentForm, BlogForm, FeedbackForm

def about(request):
    """Страница 'О магазине' (главная)"""
    return render(request, 'app/about.html', {
        'year': datetime.now().year,
    })

def links(request):
    """Страница с полезными ссылками"""
    return render(request, 'app/links.html', {
        'year': datetime.now().year,
    })

def pool(request):
    """Страница обратной связи с формой"""
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'app/pool.html', {
                'form': None,
                'submitted': True,
                'data': form.cleaned_data,
                'year': datetime.now().year,
            })
    else:
        form = FeedbackForm()
    
    return render(request, 'app/pool.html', {
        'form': form,
        'submitted': False,
        'year': datetime.now().year,
    })

def blog(request):
    """Страница со списком статей блога"""
    posts = Blog.objects.all().order_by('-posted')
    return render(request, 'app/blog.html', {
        'title': 'Блог',
        'posts': posts,
        'year': datetime.now().year,
    })

def blogpost(request, parameter):  # ← parametr → parameter
    """Страница отдельной статьи с комментариями"""
    post_1 = Blog.objects.get(id=parameter)
    comments = Comment.objects.filter(post=parameter).order_by('-date')
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user
            comment_f.date = datetime.now()
            comment_f.post = post_1
            comment_f.save()
            return redirect('blogpost', parameter=post_1.id)
    else:
        form = CommentForm()
    
    return render(request, 'app/blogpost.html', {
        'post_1': post_1,
        'comments': comments,
        'form': form,
        'year': datetime.now().year,
    })
def newpost(request):
    """Добавление новой статьи (только для администратора)"""
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('home')
    
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.posted = datetime.now()
            post.save()
            return redirect('blog')
    else:
        form = BlogForm()
    
    return render(request, 'app/newpost.html', {
        'form': form,
        'year': datetime.now().year,
    })

def videopost(request):
    """Страница с видео"""
    return render(request, 'app/videopost.html', {
        'year': datetime.now().year,
    })

def registration(request):
    """Регистрация нового пользователя"""
    if request.method == "POST":
        regform = UserCreationForm(request.POST)
        if regform.is_valid():
            regform.save()
            return redirect('login')
    else:
        regform = UserCreationForm()
    
    return render(request, 'app/registration.html', {
        'regform': regform,
        'year': datetime.now().year,
    })