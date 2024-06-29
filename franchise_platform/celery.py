from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Sett standard Django settings-modul for 'celery' programmet.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'franchise_platform.settings')

app = Celery('franchise_platform')

# Bruk en streng her slik at worker ikke må serialisere konfigurasjonsobjektet til barnens prosesser.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Oppdag tasks-moduler i Django-apps.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
