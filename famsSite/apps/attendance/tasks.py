from celery.task import periodic_task
from celery.schedules import crontab
from django.utils import timezone
from .models import Schedule

@periodic_task(run_every=crontab(hour=0, minute=0))
def update_model_data():
    # Retrieve the data to be updated
    data = 'VACANT'
    
    # Update the model
    for obj in Schedule.objects.all():
        obj.attendance_status = data
        obj.save()
