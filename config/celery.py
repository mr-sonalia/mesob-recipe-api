import os

from celery import Celery
from celery.schedules import crontab

from .settings.base import CELERY_BROKER_URL, INSTALLED_APPS

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

celery_app = Celery(
    "recipe_api",
    broker=CELERY_BROKER_URL,
)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
celery_app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
celery_app.autodiscover_tasks(lambda: INSTALLED_APPS)

# celery_app.conf.beat_schedule = {
#     "send-email-everyday": {
#         "task": "users.tasks.send_bulk_email_task",
#         "schedule": crontab(hour=0, minute=0),
#     },
# }
