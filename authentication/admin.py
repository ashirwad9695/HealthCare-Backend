from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('name', 'email')
    list_filter = ('is_staff', 'is_active')
    ordering = ('-date_joined',)
