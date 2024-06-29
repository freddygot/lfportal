from django.contrib import admin
from .models import Appointment
from .tasks import send_feedback_email

@admin.action(description='Send feedback email')
def send_feedback_email_action(modeladmin, request, queryset):
    for appointment in queryset:
        send_feedback_email(appointment.id)
    modeladmin.message_user(request, "Feedback email sent successfully.")

try:
    admin.site.unregister(Appointment)
except admin.sites.NotRegistered:
    pass

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'psychologist', 'client', 'date', 'time')
    actions = [send_feedback_email_action]
