from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('step1/', views.step1_view, name='step1'),
    path('step2/', views.step2_view, name='step2'),
    path('step3/', views.step3_view, name='step3'),
    path('complete_step4/', views.complete_step4, name='complete_step4'),
    path('success/', views.success_view, name='success'),
    path('error/', views.error_view, name='error'),  # Добавьте этот путь
    path('applications/export/', views.export_applications_to_excel, name='export_applications_to_excel'),
    path('applications/list/', views.applications_list, name='applications_list'),

]
