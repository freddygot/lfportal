from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils import timezone
from journals.models import Appointment  # Sørg for riktig import uten sirkulær avhengighet
from feedback.tasks import schedule_feedback_email

@receiver(post_save, sender=Appointment)
def create_feedback_email(sender, instance, created, **kwargs):
    if created:
        schedule_feedback_email.apply_async((instance.id,), eta=instance.date - timezone.timedelta(hours=1))

@receiver(pre_delete, sender=Appointment)
def delete_feedback_email(sender, instance, **kwargs):
    # Plassholder for sletting av feedback email oppgave om nødvendig
    pass
