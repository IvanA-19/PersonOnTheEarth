from django import forms

class FeedbackForm(forms.Form):
    name = forms.CharField(
        label="Имя",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    contact_method = forms.CharField(
        label="Способ связи (телефон или email)",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    topic_choices = [
        ('question', 'Вопрос организаторам'),
        ('suggestion', 'Предложения по программе'),
        ('review', 'Отзыв о мероприятии'),
        ('other', 'Прочее'),
    ]
    topic = forms.ChoiceField(
        label="Тема сообщения",
        choices=topic_choices,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    message = forms.CharField(
        label="Сообщение",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5})
    )