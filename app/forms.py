"""
Definition of forms for Autoparts.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Comment, Blog, Feedback

class BootstrapAuthenticationForm(AuthenticationForm):
    """Форма авторизации с Bootstrap styling"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class CommentForm(forms.ModelForm):
    """Форма добавления комментария"""
    
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {'text': 'Комментарий'}
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Ваш комментарий...'})
        }

class BlogForm(forms.ModelForm):
    """Форма добавления статьи блога"""
    
    class Meta:
        model = Blog
        fields = ('title', 'description', 'content', 'image')
        labels = {
            'title': 'Заголовок статьи',
            'description': 'Краткое содержание',
            'content': 'Полное содержание',
            'image': 'Изображение для статьи',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 100%;'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'content': forms.Textarea(attrs={'rows': 10, 'class': 'form-control'}),
        }

class FeedbackForm(forms.ModelForm):
    """Форма обратной связи"""
    
    rating = forms.ChoiceField(
        choices=Feedback.RATING_CHOICES,
        widget=forms.RadioSelect,
        label="Оценка работы сайта"
    )
    frequency = forms.ChoiceField(
        choices=Feedback.FREQUENCY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Как часто вы посещаете наш сайт?"
    )
    improvements = forms.MultipleChoiceField(
        choices=Feedback.IMPROVEMENTS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Что нужно улучшить?"
    )
    
    class Meta:
        model = Feedback
        fields = ('name', 'email', 'rating', 'frequency', 'improvements', 'suggestions')
        labels = {
            'name': 'Ваше имя',
            'email': 'Email для связи',
            'suggestions': 'Ваши пожелания и предложения',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иван Иванов'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ivan@example.com'}),
            'suggestions': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Расскажите, что нам стоит улучшить...'}),
        }
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 2:
            raise forms.ValidationError('Имя должно содержать минимум 2 символа')
        return name