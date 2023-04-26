from django_apscheduler import util
from django_apscheduler.models import DjangoJobExecution
from attendance.models import Schedule, Employee_DTR, Employee_Absence_Record
from datetime import datetime, date
import logging
import pytz

logger = logging.getLogger(__name__)
timezone = pytz.timezone('Asia/Manila')

@util.close_old_connections
def delete_old_job_executions(max_age=3600):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)

def update_sched_job():
    done_scheds = Schedule.objects.filter(status="DONE")
        
    for sched in done_scheds:
        expiration = datetime.strptime(str(sched.expiration_date), '%Y-%m-%d')
        current_date = date.today()

        if str(sched.weekday).upper() == datetime.now(timezone).strftime('%A').upper() and current_date <= expiration.date():
            sched.status = "PENDING"
            sched.save()
        else:
            sched.status = "EXPIRED"
            sched.save()
    logger.info("SCHEDULE STATUS UPDATED...")
    
def sched_time_out_tracker_job():
    ongoing_dtrs = Employee_DTR.objects.filter(status="ONGOING")
    
    for dtr in ongoing_dtrs:
        if dtr.schedule.time_out < datetime.now(timezone).time():
            dtr.time_out = datetime.now(timezone)
            dtr.save()
        else:
            logger.info("DTR TIME OUT ALREADY UPDATED...")
    logger.info("DTR TIME OUT UPDATED...")

def absent_sched_tracker_job():
    vacant_scheds = Schedule.objects.filter(status="PENDING")
    for sched in vacant_scheds:
        if str(sched.weekday).upper() == datetime.now(timezone).strftime('%A').upper() and sched.time_out <= datetime.now(timezone).time():
            Employee_Absence_Record.objects.create(
                schedule = sched,
                employee = sched.employee
            )
            sched.status = "ABSENT"
            sched.save()
        else:
            logger.info("ABSENT SCHED ALREADY UPDATED...")
    logger.info("SCHED UPDATED...")