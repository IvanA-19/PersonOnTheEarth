from django import forms

from django import forms

class AddLeaderForm(forms.Form):
    full_name = forms.CharField(max_length=200, label="ФИО руководителя", required=False)  # Поле обязательно
    position = forms.CharField(max_length=200, label="Должность", required=False)
    academic_title = forms.CharField(max_length=100, label="Ученое звание", required=False)
    workplace = forms.CharField(max_length=200, label="Место работы", required=False)
    mobile_phone = forms.CharField(max_length=20, label="Мобильный телефон", required=False)  # Поле обязательно
    other_contact = forms.CharField(max_length=200, label="Другой способ связи", required=False)

    def clean(self):
        cleaned_data = super().clean()
        full_name = cleaned_data.get('full_name')
        mobile_phone = cleaned_data.get('mobile_phone')

        if not full_name and not mobile_phone:
            raise forms.ValidationError("Пожалуйста, укажите ФИО руководителя и/или Мобильный телефон.")

        return cleaned_data

class AddParticipantForm(forms.Form):
    PARTICIPATION_CHOICES = [
        ('', 'Не выбрано'),
        ('school', 'Школа'),
        ('additional_education', 'Учреждение дополнительного образования'),
    ]

    full_name = forms.CharField(max_length=200, label="Фамилия, имя", required=False)
    birth_date = forms.DateField(label="Дата рождения", required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    participation_type = forms.ChoiceField(
        label="Тип участия",
        choices=PARTICIPATION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),  # Bootstrap styling
        required=False
    )
    school = forms.CharField(max_length=100, label="Школа", required=False)
    grade = forms.CharField(max_length=10, label="Класс", required=False)
    additional_education_name = forms.CharField(max_length=200, label="Наименование учреждения", required=False)
    age = forms.IntegerField(label="Возраст", required=False)
    project = forms.CharField(max_length=100, label='Тема проекта', required=False)

    def clean(self):
        cleaned_data = super().clean()
        participation_type = cleaned_data.get('participation_type')
        school = cleaned_data.get('school')
        grade = cleaned_data.get('grade')
        additional_education_name = cleaned_data.get('additional_education_name')
        age = cleaned_data.get('age')

        if participation_type == 'school':
            if not school or not grade:
                self.add_error('school', "Пожалуйста, укажите школу и класс.")
                self.add_error('grade', "Пожалуйста, укажите школу и класс.")
        elif participation_type == 'additional_education':
            if not additional_education_name or not age:
                self.add_error('additional_education_name', "Пожалуйста, укажите наименование учреждения и возраст.")
                self.add_error('age', "Пожалуйста, укажите наименование учреждения и возраст.")

        return cleaned_data

class Step1Form(forms.Form):
    REGION_CHOICES = [
        ('', 'Не выбран'),
        ('adg', 'Республика Адыгея'),
        ('alt', 'Алтайский край'),
        ('amr', 'Амурская область'),
        ('ark', 'Архангельская область'),
        ('ast', 'Астраханская область'),
        ('bel', 'Белгородская область'),
        ('bry', 'Брянская область'),
        ('vld', 'Владимирская область'),
        ('vlg', 'Волгоградская область'),
        ('volog', 'Вологодская область'),
        ('vor', 'Воронежская область'),
        ('iva', 'Ивановская область'),
        ('irk', 'Иркутская область'),
        ('kbd', 'Кабардино-Балкарская Республика'),
        ('kln', 'Калининградская область'),
        ('klg', 'Калужская область'),
        ('kam', 'Камчатский край'),
        ('kar', 'Карачаево-Черкесская Республика'),
        ('kem', 'Кемеровская область'),
        ('kir', 'Кировская область'),
        ('kos', 'Костромская область'),
        ('kras', 'Краснодарский край'),
        ('krs', 'Красноярский край'),
        ('kur', 'Курганская область'),
        ('kursk', 'Курская область'),
        ('len', 'Ленинградская область'),
        ('lip', 'Липецкая область'),
        ('mag', 'Магаданская область'),
        ('mow', 'Московская область'),
        ('mur', 'Мурманская область'),
        ('niz', 'Нижегородская область'),
        ('nvg', 'Новгородская область'),
        ('nsk', 'Новосибирская область'),
        ('oms', 'Омская область'),
        ('orb', 'Оренбургская область'),
        ('orl', 'Орловская область'),
        ('pen', 'Пензенская область'),
        ('perm', 'Пермский край'),
        ('pri', 'Приморский край'),
        ('psk', 'Псковская область'),
        ('ros', 'Ростовская область'),
        ('rya', 'Рязанская область'),
        ('sam', 'Самарская область'),
        ('sar', 'Саратовская область'),
        ('sak', 'Сахалинская область'),
        ('svl', 'Свердловская область'),
        ('smo', 'Смоленская область'),
        ('tamb', 'Тамбовская область'),
        ('tver', 'Тверская область'),
        ('tom', 'Томская область'),
        ('tul', 'Тульская область'),
        ('tyu', 'Тюменская область'),
        ('udm', 'Удмуртская Республика'),
        ('uly', 'Ульяновская область'),
        ('khab', 'Хабаровский край'),
        ('khak', 'Республика Хакасия'),
        ('khm', 'Ханты-Мансийский автономный округ'),
        ('chel', 'Челябинская область'),
        ('che', 'Чеченская Республика'),
        ('chu', 'Чувашская Республика'),
        ('chuk', 'Чукотский автономный округ'),
        ('yan', 'Ямало-Ненецкий автономный округ'),
        ('yar', 'Ярославская область'),
        ('sev', 'Севастополь'),
        ('krm', 'Республика Крым'),
        ('msc', 'Москва'),
        ('spb', 'Санкт-Петербург'),
        ('ynk', 'Республика Тыва (Тува)'),
        ('dag', 'Республика Дагестан'),
        ('ing', 'Республика Ингушетия'),
        ('kalm', 'Республика Калмыкия'),
        ('mrd', 'Республика Мордовия'),
        ('sah', 'Республика Саха (Якутия)'),
        ('tatar', 'Республика Татарстан'),
        ('bur', 'Республика Бурятия'),
        ('altres', 'Республика Алтай'),
        ('zab', 'Забайкальский край'),
        ('sta', 'Ставропольский край'),
        ('kmr', 'Республика Коми'),
        ('nnao', 'Ненецкий автономный округ'),
        ('amu', 'Республика Марий Эл')
    ]
    region = forms.ChoiceField(choices=REGION_CHOICES, label="Регион", required=True)
    city = forms.CharField(max_length=100, label="Населенный пункт")
    organization_name = forms.CharField(max_length=200, label="Название организации")
    postal_address = forms.CharField(max_length=200, label="Почтовый адрес")
    phone_number = forms.CharField(max_length=20, label="Телефон с кодом города")
    email = forms.EmailField(label="Электронная почта")
    website = forms.URLField(required=False, label="Сайт (необязательно)")

class Step2Form(forms.Form):
    comment = forms.CharField(widget=forms.Textarea, label="Вопросы, предложения, пожелания", max_length=500, required=False)