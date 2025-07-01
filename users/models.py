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
    full_name = models.CharField(max_length=200, verbose_name="Фамилия, имя")
    birth_date = models.DateField(verbose_name="Дата рождения")

    PARTICIPATION_CHOICES = [
        ("school", "Школа"),
        ("college", "Колледж/ВУЗ"),
        ("additional", "Учреждение ДО"),
        ("family", "Семейный коллектив"),
        ("movement", "Движение"),
        # Добавляем варианты для номинации №6
        ("kindergarten", "Детский сад"),
        ("family_education", "Семейное воспитание"),
    ]

    participation_type = models.CharField(
        max_length=20, choices=PARTICIPATION_CHOICES, verbose_name="Тип участия"
    )

    family_name = models.CharField(
        max_length=200, verbose_name="Название семейного коллектива (фамилия)", blank=True, null=True
    )

    school_name = models.CharField(
        max_length=200, verbose_name="Школа", blank=True, null=True
    )
    grade = models.CharField(max_length=10, verbose_name="Класс", blank=True, null=True)

    college_name = models.CharField(
        max_length=200, verbose_name="Колледж/ВУЗ", blank=True, null=True
    )
    course = models.CharField(max_length=50, verbose_name="Курс", blank=True, null=True)

    additional_education_name = models.CharField(
        max_length=200, verbose_name="Учреждение ДО", blank=True, null=True
    )

    MOVEMENT_CHOICES = [
        ("children", "Детское"),
        ("youth", "Молодежное"),
    ]

    movement_type = models.CharField(
        max_length=20, choices=MOVEMENT_CHOICES, verbose_name="Тип движения", blank=True, null=True
    )

    # Новые поля для дополнительных типов участия
    kindergarten_name = models.CharField(
        max_length=200, verbose_name="Детский сад", blank=True, null=True
    )
    family_education_surname = models.CharField(
        max_length=200, verbose_name="Фамилия (для семейного воспитания)", blank=True, null=True
    )

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Участник"
        verbose_name_plural = "Участники"



class Application(models.Model):
    NOMINATION_CHOICES = [
        ("1", "НОМИНАЦИЯ № 1. «ПРОБЛЕМЫ ПРИРОДНЫХ ЭКОСИСТЕМ»"),
        ("2", "НОМИНАЦИЯ № 2. «ЖИВОТНЫЕ И РАСТЕНИЯ В ЭКОСИСТЕМАХ»"),
        ("3", "НОМИНАЦИЯ № 3. «ЭТНОГРАФИЧЕСКИЕ ИССЛЕДОВАНИЯ»"),
        ("4", "НОМИНАЦИЯ № 4. «ЭКОЛОГИЧЕСКИЕ ПРОБЛЕМЫ ПОСЕЛЕНИЙ.ПРОБЛЕМЫ ЭКОНОМИИ ЭНЕРГИИ И РЕСУРСОВ»"),
        ("5", "НОМИНАЦИЯ № 5. «ЭКОТЕХ: ТЕХНОЛОГИИ ВО БЛАГО ПРИРОДЫ»"),
        ("6", "НОМИНАЦИЯ № 6. «ПЕРВЫЕ ШАГИ В ЭКОЛОГИИ»"),
    ]

    region = models.CharField(max_length=100, verbose_name="Регион")
    city = models.CharField(max_length=100, verbose_name="Населенный пункт")
    organization_name = models.CharField(max_length=200, verbose_name="Название организации")
    postal_address = models.CharField(max_length=200, verbose_name="Почтовый адрес")
    phone_number = models.CharField(max_length=20, verbose_name="Телефон с кодом города")
    email = models.EmailField(verbose_name="Электронная почта")
    website = models.URLField(blank=True, null=True, verbose_name="Сайт (необязательно)")
    comment = models.CharField(verbose_name="Комментарий", max_length=500, null=True, blank=True)
    leaders = models.ManyToManyField(Leader, blank=True, verbose_name="Руководители")
    participants = models.ManyToManyField(Participant, blank=True, verbose_name="Участники")

    project_title = models.CharField(max_length=400, verbose_name="Тема проекта", blank=True, null=True)
    nomination = models.CharField(max_length=1, choices=NOMINATION_CHOICES, verbose_name="Номинация", blank=True,
                                  null=True)

    registration_number = models.PositiveIntegerField(verbose_name="Регистрационный номер", unique=True, blank=True,
                                                      null=True)

    def save(self, *args, **kwargs):
        if not self.registration_number:
            last = Application.objects.order_by('-registration_number').first()
            self.registration_number = (last.registration_number + 1) if last and last.registration_number else 140001
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.organization_name} ({self.city})"

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
