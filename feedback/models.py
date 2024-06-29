from django.db import models
from journals.models import Client, Appointment






class Feedback(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    personal = models.IntegerField()
    interpersonal = models.IntegerField()
    social = models.IntegerField()
    general = models.IntegerField()
    total_score = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_score = self.personal + self.interpersonal + self.social + self.general
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Feedback for {self.client.name} on {self.date}'
