from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'Администратор'),
        (2, 'Пользователь'),
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Имя пользователя'
    )
    email = models.EmailField(
        unique=True,
        verbose_name='Электронная почта'
    )

    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Фамилия'
    )

    user_type = models.PositiveSmallIntegerField(
        choices=USER_TYPE_CHOICES,
        default=2,
        verbose_name='Тип пользователя')

    def is_admin(self):
        return self.user_type == 1

    def save(self, *args, **kwargs):
        if self.user_type == 1:
            self.is_staff = True
            self.is_superuser = True
        else:
            self.is_staff = False
            self.is_superuser = False
        super().save(*args, **kwargs)

    class Meta:
        # чтобы избежать конфликтов
        db_table = 'accounts_customuser'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
