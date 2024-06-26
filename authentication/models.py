from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=30, choices=[('franchise_taker', 'Franchise-taker'), ('employee', 'Ansatt')])
    key_metrics = models.JSONField(default=dict, blank=True, null=True)  # Gjør feltet ikke-obligatorisk

    def __str__(self):
        return f"{self.user.username} - {self.role}"
