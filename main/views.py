from .models import *
from django.shortcuts import render
from .forms import FeedbackForm

def index_view(request):
    news_list = News.objects.all().order_by('-publication_date')[:3] # последние 3 новости

    return render(request, 'main/index.html', {'news_list': news_list})

def news_view(request):
    news_list = News.objects.all()  # Получаем все новости из базы данных
    return render(request, 'main/news.html', {'news_list': news_list})  # Передаем список новостей в шаблон

def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # Получаем данные из формы
            name = form.cleaned_data['name']
            contact_method = form.cleaned_data['contact_method']
            topic = form.cleaned_data['topic']
            message = form.cleaned_data['message']

            # Сохраняем сообщение в базу данных
            feedback_message = FeedbackMessage(
                name=name,
                contact_method=contact_method,
                topic=topic,
                message=message
            )
            feedback_message.save()

            return render(request, 'main/success.html')  # Перенаправляем на страницу успеха
    else:
        form = FeedbackForm()

    return render(request, 'main/feedback.html', {'form': form})

def success_view(request):
    return render(request, 'main/success.html')