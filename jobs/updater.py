import logging
import pytz
import uuid
from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from .jobs import update_sched_job, sched_time_out_tracker_job, delete_old_job_executions

logger = logging.getLogger(__name__)
timezone = pytz.timezone('Asia/Manila')

scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
scheduler.add_jobstore(DjangoJobStore(), "default")
job_id = str(uuid.uuid4()) # generate a UUID for the job ID

def start_jobs():
    scheduler.add_job(
        update_sched_job,
        trigger=CronTrigger(hour='0', minute='0'),  # Every midnight
        id="update_sched_job_{}".format(job_id),  # The `id` assigned to each job MUST be unique
        max_instances=1,
        replace_existing=True,
    )
    logger.info("Added job 'update_sched_job'.")

    scheduler.add_job(
        sched_time_out_tracker_job,
        trigger=CronTrigger(minute='*/5'), # Run every 5 mins
        id="sched_time_out_tracker_job_{}".format(job_id),
        max_instance=1,
        replace_existing=True,
        misfire_grace_time=64,
    )
    logger.info("Added job 'sched_time_out_tracker_job'.")

    scheduler.add_job(
        delete_old_job_executions,
        trigger=CronTrigger(
            hour="0", minute="0"
        ),  # Midnight on Monday, before start of the next work week.
        id="delete_old_job_executions_{}".format(job_id),
        max_instances=1,
        replace_existing=True,
        misfire_grace_time=3600,
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