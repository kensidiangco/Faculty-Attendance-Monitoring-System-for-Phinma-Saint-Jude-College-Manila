from attendance.models import Schedule
from celery import shared_task

@shared_task
def update_schedule_status():
    schedules = Schedule.objects.filter(status='DONE')
    for schedule in schedules:
        schedule.status = 'VACANT'
        schedule.save()