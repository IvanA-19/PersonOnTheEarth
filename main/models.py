from django.db import models

from django.db import models

class News(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    publication_date = models.DateTimeField(auto_now=True, verbose_name='Дата публикации')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-publication_date']

class FeedbackMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    contact_method = models.CharField(max_length=100, verbose_name="Способ связи")
    topic = models.CharField(max_length=50, verbose_name="Тема сообщения")
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Сообщение от {self.name} ({self.topic})"

    class Meta:
        verbose_name = "Сообщение обратной связи"
        verbose_name_plural = "Сообщения обратной связи"
        ordering = ['-created_at']
