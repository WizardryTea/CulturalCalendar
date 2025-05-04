# server/affiche/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Theater, Performance, Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    def performance_with_date(self, obj):
        return format_html(
            '{}<br><small class="text-muted">{}</small>',
            obj.performance.title,
            obj.performance.date.strftime('%d.%m.%Y %H:%M')
        )
    performance_with_date.short_description = 'Постановка'
    performance_with_date.admin_order_field = 'performance__date'

    list_display = ('text', 'author', 'performance_with_date', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'author', 'performance')
    search_fields = ('text', 'author__username', 'performance__title')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    
    fields = ('text', 'author', 'performance', 'created_at', 'updated_at')
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Редактирование существующего комментария
            return ()  # Все поля редактируемые
        return ()  # Создание нового комментария

admin.site.register(Theater)
admin.site.register(Performance)