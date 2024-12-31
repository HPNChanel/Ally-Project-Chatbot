
from celery import shared_task
from django.utils.timezone import now
from .models import UserSettings, ChatHistory

@shared_task
def send_reminders():
  #* Send reminder as app message
  current_time = now().time()
  reminders = UserSettings.objects.filter(reminders_enabled=True, reminder_time=current_time)
  
  for reminder in reminders:
    #* Save to history
    ChatHistory.objects.create(
      user=reminder.user,
      message=reminder.reminder_message,
      is_bot=True
    )