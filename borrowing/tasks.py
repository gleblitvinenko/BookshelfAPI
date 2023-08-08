from django.utils import timezone
from django_q.models import Schedule
# from bot import send_overdue_and_upcoming_notifications


def create_daily_task():
    Schedule.objects.create(
        func="bot.send_overdue_and_upcoming_notifications",
        schedule_type=Schedule.MINUTES,
        minutes=1,
        repeats=5,
        next_run=timezone.now(),
    )
