
from celery import shared_task
from django.utils.timezone import now
from .models import UserSettings, ChatHistory

@shared_task
def send_reminders():
  pass