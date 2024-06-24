from django.db import models
from django.contrib.auth.models import User

class Kurs(models.Model):
    navn = models.CharField(max_length=200)
    beskrivelse = models.TextField()

    def __str__(self):
        return self.navn

class Modul(models.Model):
    kurs = models.ForeignKey(Kurs, related_name='moduler', on_delete=models.CASCADE)
    navn = models.CharField(max_length=200)
    innhold = models.TextField()

    def __str__(self):
        return self.navn

class FullfortModul(models.Model):
    bruker = models.ForeignKey(User, on_delete=models.CASCADE)
    modul = models.ForeignKey(Modul, on_delete=models.CASCADE)
    fullfort = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.bruker.username} - {self.modul.navn}'
