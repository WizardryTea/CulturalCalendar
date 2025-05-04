from django import forms
from .models import Performance, Comment
from django.forms import inlineformset_factory


class PerformanceForm(forms.ModelForm):
    class Meta:
        model = Performance
        fields = [
            'title', 'theater', 'date', 'description',
            'image_url', 'source_url', 'genre', 
            'min_age', 'is_premiere', 'duration', 'stage'
        ]
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'duration': forms.TextInput(attrs={
                'placeholder': 'HH:MM:SS или оставьте пустым'
            }),
            'stage': forms.TextInput(attrs={
                'placeholder': 'Например: Основная сцена'
            }),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Оставьте ваш комментарий...'
            })
        }