from __future__ import absolute_import, unicode_literals

# Dette vil sikre at appen alltid importeres når Django starter slik at shared_task vil bruke denne appen.
from .celery import app as celery_app

__all__ = ('celery_app',)
