from django.db import models
from django.contrib.auth.models import User

class Kurs(models.Model):
    navn = models.CharField(max_length=100)
    beskrivelse = models.TextField()

    def __str__(self):
        return self.navn

class Modul(models.Model):
    kurs = models.ForeignKey(Kurs, related_name='moduler', on_delete=models.CASCADE)
    navn = models.CharField(max_length=100)
    beskrivelse = models.TextField()

    def __str__(self):
        return self.navn

class FullfortModul(models.Model):
    bruker = models.ForeignKey(User, on_delete=models.CASCADE)
    modul = models.ForeignKey(Modul, on_delete=models.CASCADE)
    fullfort_dato = models.DateTimeField(auto_now_add=True)

class FullfortKurs(models.Model):
    bruker = models.ForeignKey(User, on_delete=models.CASCADE)
    kurs = models.ForeignKey(Kurs, on_delete=models.CASCADE)
    fullfort_dato = models.DateTimeField(auto_now_add=True)
