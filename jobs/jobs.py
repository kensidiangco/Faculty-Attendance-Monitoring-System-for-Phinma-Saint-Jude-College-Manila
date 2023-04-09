from django_apscheduler import util
from django_apscheduler.models import DjangoJobExecution
from attendance.models import Schedule, Employee_DTR
from datetime import datetime
import logging
import pytz

logger = logging.getLogger(__name__)
timezone = pytz.timezone('Asia/Manila')

@util.close_old_connections
def delete_old_job_executions(max_age=43_200):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)

def update_sched_job():
    print("running")
    done_scheds = Schedule.objects.filter(status="DONE")
    for sched in done_scheds:
        if str(sched.weekday).upper() == datetime.now(timezone).strftime('%A').upper():
            sched.status = "VACANT"
            sched.save()
        else:
            print("SCHEDULE ALREADY UPDATED...")
            logger.info("SCHEDULE ALREADY UPDATED...")
    logger.info("SCHEDULE STATUS UPDATED...")
    
def sched_time_out_tracker_job():
    print("running")
    ongoing_dtrs = Employee_DTR.objects.filter(status="ONGOING")
    for dtr in ongoing_dtrs:
        if dtr.schedule.time_out < datetime.now(timezone).time():
            dtr.time_out = datetime.now(timezone)
            dtr.save()
        else:
            print("DTR TIME OUT ALREADY UPDATED...")
            logger.info("DTR TIME OUT ALREADY UPDATED...")
    logger.info("DTR TIME OUT UPDATED...")