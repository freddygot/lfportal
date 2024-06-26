# apps.py i authentication-appen

from django.apps import AppConfig

class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'

    def ready(self):
        import authentication.signals  # Legg til denne linjen for å sikre at signalene er koblet
