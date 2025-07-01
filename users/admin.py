from django.contrib import admin
from .models import Application, Leader, Participant

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'registration_number', 'organization_name', 'city', 'region',
        'postal_address', 'phone_number', 'email', 'website', 'project_title', 'nomination'
    )
    ordering = ['registration_number']
    search_fields = ('organization_name', 'city', 'region', 'project_title')


@admin.register(Leader)
class LeaderAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 'mobile_phone', 'position', 'academic_title', 'workplace', 'other_contact'
    )
    search_fields = ('full_name', 'mobile_phone', 'workplace')


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 'birth_date', 'participation_type',
        'school_name', 'grade',
        'college_name', 'course',
        'additional_education_name',
        'movement_type', 'family_name',
        'family_education_surname',
        'kindergarten_name'
    )
    search_fields = ('full_name', 'school_name', 'college_name', 'additional_education_name')
    list_filter = ('participation_type', 'movement_type')
