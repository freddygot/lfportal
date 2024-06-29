from celery import shared_task
from django.core.mail import send_mail
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Appointment

def send_feedback_email(appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    feedback_url = reverse('feedback_form', args=[appointment.id])
    message = f'Hi {appointment.client.name},\n\nPlease fill out the feedback form before your appointment: {feedback_url}\n\nThank you!'
    send_mail(
        'Feedback Form',
        message,
        'fredrik@lianfjell.no',  # E-posten sendes fra din faktiske e-postadresse
        [appointment.client.email],  # E-posten sendes til klientens e-postadresse
        fail_silently=False,
    )

@shared_task
def schedule_feedback_email(appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    send_time = datetime.combine(appointment.date, appointment.time) - timedelta(hours=1)
    send_time = timezone.make_aware(send_time, timezone.get_current_timezone())
    if timezone.now() >= send_time:
        send_feedback_email(appointment_id)
    else:
        schedule_feedback_email.apply_async((appointment_id,), eta=send_time)
