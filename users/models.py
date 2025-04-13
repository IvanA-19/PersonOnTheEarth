from django.db import models


class Leader(models.Model):
    """
    Модель для контактных данных руководителя делегации.
    """
    full_name = models.CharField(max_length=200, verbose_name="ФИО руководителя")
    position = models.CharField(max_length=200, verbose_name="Должность", blank=True, null=True)  # Новое поле
    academic_title = models.CharField(max_length=100, verbose_name="Ученое звание", blank=True, null=True)  # Новое поле
    workplace = models.CharField(max_length=200, verbose_name="Место работы", blank=True, null=True)  # Новое поле
    mobile_phone = models.CharField(max_length=20, verbose_name="Мобильный телефон")
    other_contact = models.CharField(max_length=200, verbose_name="Другой способ связи", blank=True)  # Необязательное поле

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Руководитель"
        verbose_name_plural = "Руководители"

class Participant(models.Model):
    """
    Модель для данных участника делегации.
    """
    full_name = models.CharField(max_length=200, verbose_name="Фамилия, имя")
    birth_date = models.DateField(verbose_name="Дата рождения")
    school = models.CharField(max_length=100, verbose_name="Школа", blank=True, null=True)
    grade = models.CharField(max_length=10, verbose_name="Класс", blank=True, null=True)
    additional_education_name = models.CharField(max_length=200, verbose_name="Наименование учреждения", blank=True, null=True)
    age = models.IntegerField(verbose_name="Возраст", blank=True, null=True)
    project = models.CharField(max_length=100, verbose_name='Тема проекта', null=True, blank=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Участник"
        verbose_name_plural = "Участники"

class Application(models.Model):
    """
    Модель для хранения информации о заявке на конкурс.
    """
    REGION_CHOICES = [
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

    region = models.CharField(max_length=10, choices=REGION_CHOICES, verbose_name="Регион")
    city = models.CharField(max_length=100, verbose_name="Населенный пункт")
    organization_name = models.CharField(max_length=200, verbose_name="Название организации")
    postal_address = models.CharField(max_length=200, verbose_name="Почтовый адрес")
    phone_number = models.CharField(max_length=20, verbose_name="Телефон с кодом города")
    email = models.EmailField(verbose_name="Электронная почта")
    website = models.URLField(blank=True, null=True, verbose_name="Сайт (необязательно)")  # Поле может быть пустым
    comment = models.CharField(verbose_name="Комментарий", max_length=500)
    leaders = models.ManyToManyField(Leader, blank=True, verbose_name="Руководители")
    participants = models.ManyToManyField(Participant, blank=True, verbose_name="Участники")

    def __str__(self):
        return f"{self.organization_name} ({self.city})"

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"