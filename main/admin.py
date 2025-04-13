from django.contrib import admin
from .models import News, FeedbackMessage


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'publication_date')  # Поля для отображения в списке новостей
    search_fields = ('title', 'text')  # Поля для поиска
    list_filter = ('publication_date',)  # Фильтры по дате
    date_hierarchy = 'publication_date'  # Навигация по датам
    prepopulated_fields = {'title': ('title',)} # Автоматическое заполнение slug из title


@admin.register(FeedbackMessage)
class FeedbackMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'topic', 'created_at')  # Поля для отображения в списке сообщений
    search_fields = ('name', 'message')  # Поля для поиска
    list_filter = ('topic', 'created_at')  # Фильтры по теме и дате
    readonly_fields = ('name', 'contact_method', 'topic', 'message', 'created_at') # Поля, доступные только для чтения

