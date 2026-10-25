"""
Definition of models for Autoparts.
"""

from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Blog(models.Model):
    """Модель статей блога"""
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Краткое содержание")
    content = models.TextField(verbose_name="Полное содержание")
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True, verbose_name="Изображение")
    posted = models.DateTimeField(default=datetime.now, verbose_name="Опубликована")
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blogpost', args=[str(self.id)])
    
    class Meta:
        verbose_name = "Статья блога"
        verbose_name_plural = "Статьи блога"
        ordering = ['-posted']

class Comment(models.Model):
    """Модель комментариев к статьям"""
    text = models.TextField(verbose_name="Текст комментария")
    date = models.DateTimeField(default=datetime.now, verbose_name="Дата добавления")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name="Статья", related_name='comments')
    
    def __str__(self):
        return f"Комментарий от {self.author} к {self.post}"
    
    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ['-date']

class Feedback(models.Model):
    """Модель отзывов пользователей"""
    RATING_CHOICES = [
        (5, 'Отлично'),
        (4, 'Хорошо'),
        (3, 'Удовлетворительно'),
        (2, 'Плохо'),
        (1, 'Ужасно'),
    ]
    
    FREQUENCY_CHOICES = [
        ('first', 'Первый раз'),
        ('weekly', 'Несколько раз в неделю'),
        ('monthly', 'Примерно раз в месяц'),
        ('rarely', 'Редко, по необходимости'),
    ]
    
    IMPROVEMENTS_CHOICES = [
        ('speed', 'Увеличить скорость работы'),
        ('design', 'Улучшить дизайн'),
        ('catalog', 'Расширить каталог запчастей'),
        ('search', 'Улучшить поиск по VIN'),
        ('delivery', 'Ускорить доставку'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name="Оценка")
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, verbose_name="Частота посещений")
    improvements = models.CharField(max_length=200, blank=True, verbose_name="Что улучшить")
    suggestions = models.TextField(blank=True, verbose_name="Пожелания")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")
    
    def __str__(self):
        return f"Отзыв от {self.name} - {self.get_rating_display()}"
    
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']