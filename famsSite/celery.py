import os
from celery import Celery
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'famsSite.settings')
app = Celery('famsSite')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.timezone = "Asia/Manila"

app.conf.beat_schedule = {
    "every_thirty_seconds": {
        "task": "attendance.tasks.thirty_seconds_func",
        "schedule": timedelta(seconds=30)
    }
}

app.autodiscover_tasks()

# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')