# models.py i authentication-appen

from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=30, choices=[('franchise_taker', 'Franchise-taker'), ('employee', 'Ansatt')])
    key_metrics = models.JSONField(default=dict)  # JSON-felt for å lagre måltall

    def __str__(self):
        return f"{self.user.username} - {self.role}"
