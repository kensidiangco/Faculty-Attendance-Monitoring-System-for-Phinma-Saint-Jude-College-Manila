import logging
import pytz
import uuid
from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from .jobs import update_sched_job, sched_time_out_tracker_job, delete_old_job_executions, absent_sched_tracker_job, update_vacant_sched
import uuid

logger = logging.getLogger(__name__)
timezone = pytz.timezone('Asia/Manila')

scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
scheduler.add_jobstore(DjangoJobStore(), "default")

def start_jobs():
    scheduler.add_job(
        update_sched_job,
        trigger=CronTrigger(hour='0', minute='0'),  
        id="update_sched_job {}".format(uuid.uuid4()),  
        max_instances=1,
        replace_existing=True,
        misfire_grace_time=3600,
    )
    logger.info("Added job 'update_sched_job'.")

    scheduler.add_job(
        sched_time_out_tracker_job,
        trigger=CronTrigger(minute='*/5'), 
        id="sched_time_out_tracker_job {}".format(uuid.uuid4()),
        max_instances=1,
        replace_existing=True,
        misfire_grace_time=3600,
    )
    logger.info("Added job 'sched_time_out_tracker_job'.")

    scheduler.add_job(
        delete_old_job_executions,
        trigger=CronTrigger(minute='*/5'),  
        id="delete_old_job_executions {}".format(uuid.uuid4()),
        max_instances=1,
        replace_existing=True,
        misfire_grace_time=3600,
    )
    logger.info("Added half day job: 'delete_old_job_executions'.")

    scheduler.add_job(
        absent_sched_tracker_job,
        trigger=CronTrigger(minute='*/5'),  
        id="absent_sched_tracker_job {}".format(uuid.uuid4()),
        max_instances=1,
        misfire_grace_time=3600,
    )
    logger.info("Added job: 'absent_sched_tracker_job'.")

    scheduler.add_job(
        update_vacant_sched,
        trigger=CronTrigger(minute='*/1'),  
        id="update_vacant_sched {}".format(uuid.uuid4()),
        max_instances=1,
        misfire_grace_time=3600,
    )
    logger.info("Added job: 'update_vacant_sched'.")

    try:
        logger.info("Starting scheduler...")
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("Stopping scheduler...")
        scheduler.shutdown()
        logger.info("Scheduler shut down successfully!")