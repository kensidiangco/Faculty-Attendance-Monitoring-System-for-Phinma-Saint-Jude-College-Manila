import uuid
from datetime import datetime, timedelta
from django.db import models

class Employee_Status(models.Model):
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = 'Employee Status'
        verbose_name_plural = 'Employee Statuses'

    def __str__(self):
        return self.name
    
class Department(models.Model):
    department_name = models.CharField(max_length=100, blank=False, null=False, unique=True)
    address = models.CharField(max_length=100, blank=False, null=False)
    room_no = models.CharField(max_length=100, blank=False, null=False)
    floor = models.CharField(max_length=100, blank=False, null=False)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.department_name

class Subject(models.Model):
    subject_code = models.CharField(max_length=100, blank=True, null=True, unique=True)
    subject_name = models.CharField(max_length=100, blank=False, null=False)
    year = models.CharField(max_length=100, blank=True, null=True)
    semester = models.CharField(max_length=100, blank=True, null=True)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.subject_name

class Employee(models.Model):
    EMPLOYEE_STATUS_CHOICES = [
        ('CONTRACTUAL', 'CONTRACTUAL'),
        ('PART TIME', 'PART TIME'),
        ('REGULAR', 'REGULAR'),
    ]
    POSITION_CHOICES = [
        ('DEAN', 'DEAN'),
        ('PROFESSOR', 'PROFESSOR'),
        ('PROGRAM HEAD', 'PROGRAM HEAD'),
    ]
    employee_ID = models.CharField(max_length=100, blank=False, null=False, unique=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    position = models.CharField(choices=POSITION_CHOICES, max_length=20, null=True)
    employee_status = models.CharField(choices=EMPLOYEE_STATUS_CHOICES, max_length=20, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='OUT')
    working_status = models.CharField(max_length=10, default='ACTIVE')
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.name

class Schedule(models.Model):
    WEEKDAY_CHOICES = [
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    weekday = models.CharField(choices=WEEKDAY_CHOICES, max_length=20)
    time_in = models.TimeField(auto_now=False, auto_now_add=False)
    time_out = models.TimeField(auto_now=False, auto_now_add=False)
    status = models.CharField(max_length=20, default='VACANT')
    expiration_date = models.DateField(null=True)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return f'{self.subject.subject_name} ({self.status})'

class Employee_DTR(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, null=True, blank=True)
    weekday = models.CharField(max_length=20, blank=True, null=True)
    time_in = models.DateTimeField(auto_now=False, auto_now_add=False)
    time_out = models.DateTimeField(null=True)
    total_working_hours = models.CharField(max_length=100, blank=True, null=True)
    attendance_status = models.CharField(max_length=25, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    date_in = models.DateField(auto_now=False, auto_now_add=True, blank=True, null=True)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = 'Employee DTR'
        verbose_name_plural = 'Employee DTRs'

    def total_hours(self):
        time_in = self.time_in
        time_out = self.time_out
        time_diff = time_out - time_in
        seconds_in_day = 24 * 60 * 60
        diff = divmod(time_diff.days * seconds_in_day + time_diff.seconds, 60)

        time_list = []
        for td in diff:
            time_list.append(td)
        h = 0
        m = time_list[0]
        s = time_list[1]
        
        if time_list[0] > 60:
            h += int(time_list[0] / 60)
            minus_mins = h * 60
            m -= minus_mins
        
        if h == 0:
            total_hours = '{}m {}s'.format(m,s)
        
        if h == 0 and m == 0:
            total_hours = '{}s'.format(s)
        
        if h != 0 and m != 0:
            total_hours = '{}h {}m {}s'.format(h,m,s)
            
        return total_hours

    def __str__(self):
        return f'{self.employee.name} ({self.date_in})'

    @classmethod
    def is_duplicate(cls, uuid):
        recent_scans = cls.objects.filter(
            uuid=uuid,
            date_created__gte=datetime.now() - timedelta(minutes=1)
        )
        return len(recent_scans) > 0