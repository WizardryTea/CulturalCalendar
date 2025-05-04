#server/accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'Admin'),
        (2, 'User'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=2)
    
    def is_admin(self):
        return self.user_type == 1
    
    def save(self, *args, **kwargs):
        # Суперпользователь всегда должен иметь is_staff=True
        if self.is_superuser:
            self.is_staff = True
        # Для обычных пользователей is_staff зависит от user_type
        elif self.user_type == 1:
            self.is_staff = True
        else:
            self.is_staff = False
        super().save(*args, **kwargs)
    
    class Meta:
        # чтобы избежать конфликтов
        db_table = 'accounts_customuser'