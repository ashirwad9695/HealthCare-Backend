from django.contrib import admin
from .models import Doctor

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'specialization', 'email', 'phone_number', 'years_of_experience', 'created_at')
    search_fields = ('name', 'specialization', 'email')
    list_filter = ('specialization', 'years_of_experience')
    ordering = ('name',)
