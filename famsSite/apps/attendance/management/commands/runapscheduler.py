import logging
import pytz
from django.conf import settings
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from ...models import Schedule, Employee_DTR

logger = logging.getLogger(__name__)
timezone = pytz.timezone('Asia/Manila')

def update_sched_job():
    done_scheds = Schedule.objects.filter(status="DONE")
    for sched in done_scheds:
        if str(sched.weekday).upper() == datetime.now().strftime('%A').upper():
            sched.status = "VACANT"
            sched.save()

    logger.info("SCHEDULE STATUS UPDATED...")
    
def sched_time_out_tracker_job():
    ongoing_dtrs = Employee_DTR.objects.filter(status="ONGOING")
    for dtr in ongoing_dtrs:
        if dtr.schedule.time_out == datetime.now().time():
            dtr.time_out = datetime.now(timezone)
            dtr.save()
            
    logger.info("DTR OUT UPDATED...")


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way. 
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)

class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            update_sched_job,
            trigger=CronTrigger(hour='0', minute='0'),  # Every midnight
            id="update_sched_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'update_sched_job'.")

        scheduler.add_job(
            sched_time_out_tracker_job,
            trigger=CronTrigger(minute='30'),
            id="sched_time_out_tracker_job",
            max_instance=1,
            replace_existing=True,
        )
        logger.info("Added job 'sched_time_out_tracker_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")