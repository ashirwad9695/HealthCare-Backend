from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'gender', 'age', 'contact_number', 'created_by', 'created_at')
    search_fields = ('name', 'contact_number', 'email')
    list_filter = ('gender', 'created_at')
    ordering = ('-created_at',)
