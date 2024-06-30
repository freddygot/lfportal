from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta

class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    psychologist = models.ForeignKey(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    personal_number = models.CharField(max_length=11, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=10, null=True, blank=True)
    municipality = models.CharField(max_length=100, null=True, blank=True)

class Service(models.Model):
    name = models.CharField(max_length=200)
    duration = models.DurationField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Journal(models.Model):
    title = models.CharField(max_length=200)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Appointment(models.Model):
    title = models.CharField(max_length=200)
    psychologist = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    journal_entry = models.OneToOneField(Journal, on_delete=models.SET_NULL, null=True, blank=True)

    def schedule_feedback_email(self):
        from feedback.tasks import schedule_feedback_email  # Import inside the method to avoid circular import
        send_time_naive = datetime.combine(self.date, self.time) - timedelta(hours=1)
        send_time = timezone.make_aware(send_time_naive, timezone.get_current_timezone())
        schedule_feedback_email.apply_async((self.id,), eta=send_time)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.schedule_feedback_email()
