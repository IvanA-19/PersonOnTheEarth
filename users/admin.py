from django.contrib import admin
from .models import Application, Leader, Participant

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('organization_name', 'city', 'region', 'postal_address', 'phone_number', 'email', 'website')


@admin.register(Leader)
class LeaderAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'mobile_phone', 'position', 'academic_title', 'workplace', 'other_contact')
    search_fields = ('full_name', 'school')

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'birth_date', 'school', 'grade', 'additional_education_name', 'age', 'project')
    search_fields = ('full_name', 'school')