# journals/admin.py
from django.contrib import admin
from .models import Client, Journal, Appointment

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'psychologist')
    search_fields = ('name', 'email', 'psychologist__username')

@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'created_at', 'updated_at')
    search_fields = ('title', 'client__name')
    list_filter = ('created_at',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'psychologist', 'client', 'date', 'time')
    search_fields = ('title', 'psychologist__username', 'client__name')
    list_filter = ('date', 'psychologist')
