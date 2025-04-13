from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from datetime import datetime
from .forms import Step1Form, Step2Form, AddLeaderForm, AddParticipantForm  # Adjust forms as needed
from .models import Application, Leader, Participant
import openpyxl
from django.http import HttpResponse

def step1_view(request):
    """Представление для первого шага: Ввод данных организации."""
    request.session.flush()

    if request.method == 'POST':
        form = Step1Form(request.POST)
        if form.is_valid():
            request.session['step1_data'] = form.cleaned_data
            return redirect(reverse('users:step2'))
    else:
        form = Step1Form()
    return render(request, 'users/step1.html', {'form': form})


def step2_view(request):
    """Представление для второго шага: Добавление руководителей."""
    step1_data = request.session.get('step1_data', None)

    if not step1_data:
        return redirect(reverse('users:step1'))

    leaders = request.session.get('leaders', [])
    add_leader_form = AddLeaderForm()

    if request.method == 'POST':
        if 'add_leader' in request.POST:
            add_leader_form = AddLeaderForm(request.POST)
            if add_leader_form.is_valid():
                leader_data = add_leader_form.cleaned_data
                leaders.append(leader_data)
                request.session['leaders'] = leaders
                add_leader_form = AddLeaderForm()  # Очищаем форму после добавления

        elif 'remove_leader' in request.POST:
            leader_index = int(request.POST['remove_leader'])
            del leaders[leader_index]
            request.session['leaders'] = leaders

        elif 'complete_step2' in request.POST:
            if leaders:
                request.session['leaders'] = leaders # Ensure leaders are saved before redirecting
                return redirect(reverse('users:step3'))
            else:
                messages.error(request, "Пожалуйста, добавьте хотя бы одного руководителя.")

    context = {
        'leaders': leaders,
        'add_leader_form': add_leader_form,
    }
    return render(request, 'users/step2.html', context)


def step3_view(request):
    """Представление для третьего шага: Добавление участников."""
    step1_data = request.session.get('step1_data', None)
    leaders = request.session.get('leaders', None)

    if not all([step1_data, leaders]):
        if step1_data is None:
            return redirect(reverse('users:step1'))
        else:
            return redirect(reverse('users:step2'))


    participants = request.session.get('participants', [])
    add_participant_form = AddParticipantForm()

    if request.method == 'POST':
        if 'add_participant' in request.POST:
            add_participant_form = AddParticipantForm(request.POST)
            if add_participant_form.is_valid():
                participant_data = add_participant_form.cleaned_data
                # Преобразуем birth_date в строку
                participant_data['birth_date'] = participant_data['birth_date'].strftime('%Y-%m-%d')
                participants.append(participant_data)
                request.session['participants'] = participants
                add_participant_form = AddParticipantForm()  # Clear the form

        elif 'remove_participant' in request.POST:
            participant_index = int(request.POST['remove_participant'])
            del participants[participant_index]
            request.session['participants'] = participants

        elif 'complete_step3' in request.POST:
            if participants:
                request.session['participants'] = participants
                return redirect(reverse('users:complete_step4'))
            else:
                messages.error(request, "Пожалуйста, добавьте хотя бы одного участника.")

    context = {
        'participants': participants,
        'add_participant_form': add_participant_form,
    }
    return render(request, 'users/step3.html', context)


def complete_step4(request):
    """Представление для четвертого шага: Ввод комментария, сохранение данных и завершение регистрации."""
    step1_data = request.session.get('step1_data', None)
    leaders = request.session.get('leaders', None)
    participants = request.session.get('participants', None)

    if not all([step1_data, leaders, participants]):
        if step1_data is None:
            return redirect(reverse('users:step1'))
        elif leaders is None:
            return redirect(reverse('users:step2'))
        else:
            return redirect(reverse('users:step3'))

    if request.method == 'POST':
        form = Step2Form(request.POST) # Step2Form now contains only comment
        if form.is_valid():
            comment = form.cleaned_data['comment']

            try:
                application = Application.objects.create(
                    region=step1_data['region'],
                    city=step1_data['city'],
                    organization_name=step1_data['organization_name'],
                    postal_address=step1_data['postal_address'],
                    phone_number=step1_data['phone_number'],
                    email=step1_data['email'],
                    website=step1_data['website'],
                    comment=comment,  # Save the comment
                )

                for leader_data in leaders:
                    # Поиск существующего руководителя
                    leader = Leader.objects.filter(
                        full_name=leader_data['full_name'],
                        position=leader_data.get('position', ''), # default value to prevent errors
                        academic_title=leader_data.get('academic_title', ''), # default value to prevent errors
                        workplace=leader_data.get('workplace', ''), # default value to prevent errors
                        mobile_phone=leader_data['mobile_phone'],
                        other_contact=leader_data.get('other_contact', ''),
                    ).first()  # Получаем первый результат или None

                    if leader is None:
                        # Руководитель не существует, создаем нового
                        leader = Leader.objects.create(
                            full_name=leader_data['full_name'],
                            position=leader_data.get('position', ''), # default value to prevent errors
                            academic_title=leader_data.get('academic_title', ''), # default value to prevent errors
                            workplace=leader_data.get('workplace', ''), # default value to prevent errors
                            mobile_phone=leader_data['mobile_phone'],
                            other_contact=leader_data.get('other_contact', ''),
                        )

                    application.leaders.add(leader)

                for participant_data in participants:
                    birth_date_str = participant_data['birth_date']
                    birth_date_dt = datetime.strptime(birth_date_str, '%Y-%m-%d').date()

                    participant = Participant.objects.create(
                        full_name=participant_data['full_name'],
                        birth_date=birth_date_dt,
                        school=participant_data.get('school', ''), # default value to prevent errors
                        grade=participant_data.get('grade', ''), # default value to prevent errors
                        project=participant_data.get('project', ''), # default value to prevent errors
                        additional_education_name=participant_data.get('additional_education_name',''),
                        age=participant_data.get('age',''),
                    )
                    application.participants.add(participant)

                request.session.flush()

                return redirect(reverse('users:success'))  # Redirect to success page

            except Exception as e:
                print(f"Error saving application: {e}")
                error_message = str(e)  # Get the error message
                return render(request, 'users/error.html', {'error_message': error_message})  # Render error page
    else:
        form = Step2Form() # Step2Form now contains only comment
        return render(request, 'users/step4.html', {'form': form})

def success_view(request):
    return render(request, 'users/success.html')

def error_view(request):
    return render(request, 'users/error.html')


def export_applications_to_excel(request):
    """
    Экспортирует данные заявок, участников и руководителей в Excel-файл.
    """

    # Получаем все заявки, отсортированные по региону
    applications = Application.objects.all().order_by('region')

    # Создаем новую книгу Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Заявки"

    # Заголовки столбцов
    headers = [
        "№",
        "Регион",
        "Город",
        "Название организации",
        "Почтовый адрес",
        "Телефон с кодом города",
        "Электронная почта",
        "Сайт",
        "Комментарий",
        # Участники
        "Участник: Фамилия, имя",
        "Участник: Дата рождения",
        "Участник: Школа",
        "Участник: Класс",
        "Участник: Наименование учреждения",
        "Участник: Возраст",
        "Участник: Тема проекта",
        # Руководители
        "Руководитель: ФИО",
        "Руководитель: Должность",
        "Руководитель: Ученое звание",
        "Руководитель: Место работы",
        "Руководитель: Мобильный телефон",
        "Руководитель: Другой способ связи",
    ]
    ws.append(headers)

    # Заполняем таблицу данными
    row_num = 2  # Начинаем со второй строки (после заголовков)
    for i, application in enumerate(applications):
        # Информация о заявке
        app_data = [
            i + 1,  # № заявки
            application.get_region_display(),  # Отображаемое значение региона
            application.city,
            application.organization_name,
            application.postal_address,
            application.phone_number,
            application.email,
            application.website or "",  # Обработка None для URLField
            application.comment,
        ]

        # Собираем информацию об участниках
        participants_data = []
        for participant in application.participants.all():
            participants_data.extend([
                participant.full_name,
                participant.birth_date.strftime('%Y-%m-%d'),  # Форматирование даты
                participant.school or "",
                participant.grade or "",
                participant.additional_education_name or "",
                participant.age or "",
                participant.project or "",
            ])

        # Собираем информацию о руководителях
        leaders_data = []
        for leader in application.leaders.all():
            leaders_data.extend([
                leader.full_name,
                leader.position or "",
                leader.academic_title or "",
                leader.workplace or "",
                leader.mobile_phone,
                leader.other_contact or "",
            ])

        # Объединяем все данные в одну строку
        row_data = app_data + participants_data + leaders_data
        ws.append(row_data)

        row_num += 1

    # Создаем HTTP-ответ для скачивания файла
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=applications.xlsx'

    # Сохраняем книгу Excel в HTTP-ответ
    wb.save(response)

    return response


@staff_member_required
def applications_list(request):
    """
    Отображает список заявок (только для администраторов).
    """
    return render(request, 'users/applications_list.html')