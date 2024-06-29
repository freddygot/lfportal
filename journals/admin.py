from django.contrib import admin
from .models import Client, Journal, Appointment, Service
from django import forms
from datetime import timedelta

class ServiceAdminForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'

    def clean_duration(self):
        duration = self.cleaned_data['duration']
        if isinstance(duration, timedelta):
            return duration
        return timedelta(minutes=duration)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.initial['duration'] = int(self.instance.duration.total_seconds() // 60)

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

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    form = ServiceAdminForm
    list_display = ('name', 'duration_in_minutes', 'price')
    search_fields = ('name',)
    list_filter = ('duration', 'price')

    def duration_in_minutes(self, obj):
        return int(obj.duration.total_seconds() // 60)
    duration_in_minutes.short_description = 'Duration (minutes)'
