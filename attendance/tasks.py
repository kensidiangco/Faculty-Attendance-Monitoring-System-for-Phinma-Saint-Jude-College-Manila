from attendance.models import Schedule
from celery import shared_task
from celery.utils.log import get_task_logger 

logger = get_task_logger(__name__)

@shared_task
def update_schedule_status():
    schedules = Schedule.objects.filter(status='DONE')
    for schedule in schedules:
        schedule.status = 'VACANT'
        schedule.save()

@shared_task
def thirty_seconds_func():
    logger.info("I run every 30 seconds using Celery Beat")
    return "DONE"