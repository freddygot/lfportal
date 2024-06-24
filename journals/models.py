# journals/models.py
from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    psychologist = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class Journal(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Appointment(models.Model):
    title = models.CharField(max_length=255)
    psychologist = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    journal_entry = models.ForeignKey(Journal, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments')

    def __str__(self):
        return f'{self.title} with {self.client} on {self.date} at {self.time}'
