from django.db import models
from journals.models import Client, Appointment

class ORSFeedback(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    question_1 = models.IntegerField()
    question_2 = models.IntegerField()
    question_3 = models.IntegerField()
    question_4 = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    @property
    def total_score(self):
        return self.question_1 + self.question_2 + self.question_3 + self.question_4
