from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('news/', views.news_view, name='news'),  # Добавляем URL для новостей
    path('feedback/', views.feedback_view, name='feedback'),  # Добавляем URL для обратной связи
    path('success/', views.success_view, name='success')
]