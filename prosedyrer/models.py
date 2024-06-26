from django.db import models
from django.contrib.auth.models import User

class Prosedyre(models.Model):
    tittel = models.CharField(max_length=255)
    beskrivelse = models.TextField()

    def __str__(self):
        return self.tittel

class ProsedyrePunkt(models.Model):
    prosedyre = models.ForeignKey(Prosedyre, on_delete=models.CASCADE)
    beskrivelse = models.TextField()
    rekkefolge = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.prosedyre.tittel} - {self.beskrivelse}"

class ProsedyreGjennomgang(models.Model):
    bruker = models.ForeignKey(User, on_delete=models.CASCADE)
    prosedyre = models.ForeignKey(Prosedyre, on_delete=models.CASCADE)
    fullført = models.BooleanField(default=False)
    fullført_dato = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.bruker.username} - {self.prosedyre.tittel}"
