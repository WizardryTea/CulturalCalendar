#server/affiche/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.validators import MinLengthValidator, URLValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import datetime, time
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

def validate_url(value):
    validator = URLValidator()
    try:
        validator(value)
    except ValidationError:
        raise ValidationError(_('Введите корректный URL'))

class Theater(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название театра")
    website = models.URLField(
        verbose_name="Ссылка",
        validators=[validate_url]
    )
    description = models.TextField(blank=True, verbose_name="Описание")
    
    class Meta:
        verbose_name = "Театр"
        verbose_name_plural = "Театры"

    def __str__(self):
        return self.name

    def clean(self):
        if self.website and not self.website.startswith(('http://', 'https://')):
            raise ValidationError({'website': _('URL должен начинаться с http:// или https://')})


class Performance(models.Model):
    title = models.CharField(
        max_length=200, 
        validators=[MinLengthValidator(3)],
        verbose_name="Название постановки"
    )
    theater = models.ForeignKey(
        Theater, 
        on_delete=models.CASCADE,
        verbose_name="Театр"
    )
    date = models.DateTimeField(verbose_name="Дата и время")
    duration = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Длительность"
    )
    stage = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Сцена"
    )
    description = models.TextField(verbose_name="Описание")
    image_url = models.URLField(
        null=True, 
        blank=True,
        verbose_name="Ссылка на изображение"
    )
    source_url = models.URLField(
        null=True, 
        blank=True,
        verbose_name="Источник"
    )
    
    @property
    def duration_display(self):
        if not self.duration:
            return "неизвестно"
        # если это строка то преобразуем в объект времени (хранится как строка)
        if isinstance(self.duration, str):
            try:
                t = datetime.strptime(self.duration, "%H:%M:%S").time()
            except ValueError:
                return "неизвестно"
        else:
            t = self.duration
        # проверяем условия для человечного вывода
        if t.hour == 0 and t.minute == 0:
            return "неизвестно"
        if t.hour == 0:
            return f"{t.minute} мин."
        return f"{t.hour} ч, {t.minute} мин."

    @property
    def formatted_date(self):
        month_names = {
            1: _('января'),
            2: _('февраля'),
            3: _('марта'),
            4: _('апреля'),
            5: _('мая'),
            6: _('июня'),
            7: _('июля'),
            8: _('августа'),
            9: _('сентября'),
            10: _('октября'),
            11: _('ноября'),
            12: _('декабря')
        }
        day = self.date.day
        month = month_names[self.date.month]
        year = self.date.year
        time = self.date.strftime("%H:%M")
        
        return f" {day} {month} {year} в {time}"

    GENRE_CHOICES = [
        ('performance', 'Спектакль'),
        ('tragicomedy', 'Трагикомедия'),
        ('drama', 'Драма'),
        ('comedy', 'Комедия'),
        ('baby', 'Для детей'),
        ('musical', 'Мюзикл'),
        ('show', 'Шоу'),
    ]
    
    genre = models.CharField(
        max_length=20,
        choices=GENRE_CHOICES,
        default='default',
        verbose_name="Жанр"
    )
    min_age = models.PositiveIntegerField(
        default=12,
        validators=[
            MinValueValidator(0, message=_('Возраст не может быть отрицательным')),
            MaxValueValidator(100, message=_('Возраст не может быть больше 100'))
        ],
        verbose_name="Минимальный возраст"
    )
    is_premiere = models.BooleanField(
        default=False,
        verbose_name="Премьера"
    )

    class Meta:
        ordering = ['date']
        verbose_name = 'Постановка'
        verbose_name_plural = 'Постановки'

    def __str__(self):
        return f"{self.title} ({self.theater.name})"

    def get_absolute_url(self):
        return reverse('affiche:performance_detail', args=[str(self.id)])

    @property
    def comment_count(self):
        return self.comments.count()

    def clean(self):
        if self.genre not in dict(self.GENRE_CHOICES):
            raise ValidationError({'genre': _('Выберите корректный жанр')})
        if self.image_url and not self.image_url.startswith(('http://', 'https://')):
            raise ValidationError({'image_url': _('URL должен начинаться с http:// или https://')})
        if self.source_url and not self.source_url.startswith(('http://', 'https://')):
            raise ValidationError({'source_url': _('URL должен начинаться с http:// или https://')})


class Comment(models.Model):
    performance = models.ForeignKey(
        Performance, 
        on_delete=models.CASCADE, 
        related_name='comments',
        verbose_name="Постановка"
    )
    author = models.ForeignKey(
        get_user_model(), 
        on_delete=models.CASCADE,
        verbose_name="Автор"
    )
    text = models.TextField(verbose_name="Текст комментария")

    created_at = models.DateTimeField(
        default=timezone.now,
        # auto_now=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Дата обновления"
    )  

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий от {self.author.username} к {self.performance.title}'
    
    def save(self, *args, **kwargs):
        if not self.id:  # Если это новый комментарий
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def can_edit(self, user):
        return user.is_staff or user == self.author

    def can_delete(self, user):
        return user.is_staff or user == self.author

