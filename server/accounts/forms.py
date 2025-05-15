# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    user_type = forms.ChoiceField(
        choices=CustomUser.USER_TYPE_CHOICES,
        widget=forms.RadioSelect,
        initial=2
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'user_type')
        labels = {
            'username': 'Имя пользователя',
            'email': 'Электронная почта',
            'user_type': 'Тип пользователя',
        }
        help_texts = {
            'username': 'Уникальное имя пользователя',
            'email': 'На 1 почту можно зарегистрировать не более 1 аккаунта',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        # user.user_type = self.cleaned_data['user_type']
        # Добавим явное преобразование user_type к int в методе save():
        user.user_type = int(self.cleaned_data['user_type'])  # преобразуем к int
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')
        labels = {
            'username': 'Имя пользователя',
            'password': 'Пароль',
        }
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}),
        }
