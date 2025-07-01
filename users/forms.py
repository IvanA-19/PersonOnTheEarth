from .models import Application, Participant
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

class AddParticipantForm(forms.ModelForm):
    kindergarten_name = forms.CharField(
        max_length=200, required=False, label="Название детского сада"
    )
    family_education_surname = forms.CharField(
        max_length=200, required=False, label="Фамилия"
    )

    class Meta:
        model = Participant
        fields = [
            "full_name",
            "birth_date",
            "participation_type",
            "school_name",
            "grade",
            "college_name",
            "course",
            "additional_education_name",
            "movement_type",
            "family_name",
            "kindergarten_name",
            "family_education_surname",
        ]
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, nomination=None, **kwargs):
        super().__init__(*args, **kwargs)

        if nomination != '6':
            # Предполагаем, что participation_type — ChoiceField
            # Фильтруем варианты, исключая детский сад и семейное воспитание
            allowed = []
            for value, label in self.fields['participation_type'].choices:
                if value not in ('kindergarten', 'family_education'):
                    allowed.append((value, label))
            self.fields['participation_type'].choices = allowed

    def clean(self):
        cleaned_data = super().clean()
        p_type = cleaned_data.get("participation_type")

        if p_type == "kindergarten":
            if not cleaned_data.get("kindergarten_name"):
                self.add_error(
                    "kindergarten_name",
                    "Это поле обязательно для заполнения при выборе «Детский сад».",
                )

        if p_type == "family_education":
            if not cleaned_data.get("family_education_surname"):
                self.add_error(
                    "family_education_surname",
                    "Это поле обязательно для заполнения при выборе «Семейное воспитание».",
                )



class Step1Form(forms.Form):
    REGION_CHOICES = [
        ('', 'Не выбран'),
        ('adg', 'Республика Адыгея'),
        ('amu', 'Республика Марий Эл'),
        ('amr', 'Амурская область'),
        ('altres', 'Республика Алтай'),
        ('alt', 'Алтайский край'),
        ('bash', 'Республика Башкортостан'),
        ('bel', 'Белгородская область'),
        ('bur', 'Республика Бурятия'),
        ('bry', 'Брянская область'),
        ('dag', 'Республика Дагестан'),
        ('dnr', 'Донецкая народная республика'),
        ('eao', 'Еврейский автономный округ'),
        ('iba', 'Ивановская область'),  # исправлено с 'iva'
        ('ing', 'Республика Ингушетия'),
        ('irk', 'Иркутская область'),
        ('kbd', 'Кабардино-Балкарская Республика'),
        ('kam', 'Камчатский край'),
        ('kalm', 'Республика Калмыкия'),
        ('kar', 'Карачаево-Черкесская Республика'),
        ('kem', 'Кемеровская область'),
        ('khak', 'Республика Хакасия'),
        ('khm', 'Ханты-Мансийский автономный округ'),
        ('khab', 'Хабаровский край'),
        ('kln', 'Калининградская область'),
        ('klg', 'Калужская область'),
        ('kmr', 'Республика Коми'),
        ('kos', 'Костромская область'),
        ('kras', 'Краснодарский край'),
        ('krs', 'Красноярский край'),
        ('kur', 'Курганская область'),
        ('kursk', 'Курская область'),
        ('lnr', 'Луганская народная республика'),
        ('len', 'Ленинградская область'),
        ('lip', 'Липецкая область'),
        ('mag', 'Магаданская область'),
        ('mow', 'Московская область'),
        ('msc', 'Москва'),
        ('mur', 'Мурманская область'),
        ('mrd', 'Республика Мордовия'),
        ('nnao', 'Ненецкий автономный округ'),
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
        ('sev', 'Севастополь'),
        ('spb', 'Санкт-Петербург'),
        ('sta', 'Ставропольский край'),
        ('svl', 'Свердловская область'),
        ('smo', 'Смоленская область'),
        ('tamb', 'Тамбовская область'),
        ('tatar', 'Республика Татарстан'),
        ('tver', 'Тверская область'),
        ('tom', 'Томская область'),
        ('tul', 'Тульская область'),
        ('tyu', 'Тюменская область'),
        ('udm', 'Удмуртская Республика'),
        ('uly', 'Ульяновская область'),
        ('yan', 'Ямало-Ненецкий автономный округ'),
        ('yar', 'Ярославская область'),
        ('ynk', 'Республика Тыва (Тува)'),
        ('zab', 'Забайкальский край'),
        ('hrn', 'Херсонская область'),
    ]

    region = forms.ChoiceField(choices=REGION_CHOICES, label="Регион", required=False)
    other_region = forms.CharField(max_length=100, label="Другой регион", required=False)

    city = forms.CharField(max_length=100, label="Населенный пункт")
    organization_name = forms.CharField(max_length=200, label="Название организации")
    postal_address = forms.CharField(max_length=200, label="Почтовый адрес")
    phone_number = forms.CharField(max_length=20, label="Телефон с кодом города")
    email = forms.EmailField(label="Электронная почта")
    website = forms.URLField(required=False, label="Сайт (необязательно)")

    def clean(self):
        cleaned_data = super().clean()
        region_code = cleaned_data.get('region')
        other_region = cleaned_data.get('other_region')

        if region_code == '' and not other_region:
            raise forms.ValidationError("Если регион не выбран, пожалуйста, укажите 'Другой регион'.")

        # Если регион не выбран, подменяем код на текст из другого региона
        if region_code == '' and other_region:
            cleaned_data['region'] = other_region
        else:
            region_dict = dict(self.REGION_CHOICES)
            if region_code in region_dict:
                cleaned_data['region'] = region_dict[region_code]
            else:
                # Если код не найден в списке — ошибка или оставляем как есть
                self.add_error('region', 'Выбран недопустимый регион.')

        return cleaned_data

class Step2Form(forms.Form):
    comment = forms.CharField(widget=forms.Textarea, label="Вопросы, предложения, пожелания", max_length=500, required=False)

class ProjectInfoForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["project_title", "nomination"]
        widgets = {
            "project_title": forms.TextInput(attrs={"class": "form-control"}),
            "nomination": forms.Select(attrs={"class": "form-control"}),
        }

