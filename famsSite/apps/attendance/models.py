import uuid
from datetime import datetime, timedelta
from django.db import models

class Employee_Status(models.Model):
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, auto_now_add=False)

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

class Employee_Position(models.Model):
    position = models.CharField(max_length=100, blank=False, null=False)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.position

class Subject(models.Model):
    subject_code = models.CharField(max_length=100, blank=True, null=True, unique=True)
    subject_name = models.CharField(max_length=100, blank=False, null=False)
    year = models.CharField(max_length=100, blank=True, null=True)
    semester = models.CharField(max_length=100, blank=True, null=True)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.subject_name

class Weekday(models.Model):
    Weekday = models.CharField(max_length=100, blank=False, null=False, unique=True)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.Weekday

class Employee(models.Model):
    employee_ID = models.CharField(max_length=100, blank=False, null=False)
    name = models.CharField(max_length=100, blank=False, null=False)
    position = models.ForeignKey(Employee_Position, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    employee_status = models.ForeignKey(Employee_Status, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, default="out")
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.name

class Schedule(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    weekday = models.ForeignKey(Weekday, on_delete=models.CASCADE)
    time_in = models.TimeField(auto_now=False, auto_now_add=False)
    time_out = models.TimeField(auto_now=False, auto_now_add=False)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.subject.subject_name

class Employee_DTR(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="employee")
    weekday = models.CharField(max_length=20, blank=True, null=True)
    time_in = models.DateTimeField(auto_now=False, auto_now_add=True)
    time_out = models.DateTimeField(null=True)
    total_working_hours = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    date_in = models.DateField(auto_now=False, auto_now_add=True, blank=True, null=True)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, auto_now_add=False)

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
            total_hours = "{}m {}s".format(m,s)
        
        if h == 0 and m == 0:
            total_hours = "{}s".format(s)
        
        if h != 0 and m != 0:
            total_hours = "{}h {}m {}s".format(h,m,s)
            
        return total_hours

    def __str__(self):
        return f"{self.employee.name} ({self.date_in})"

    @classmethod
    def is_duplicate(cls, uuid):
        recent_scans = cls.objects.filter(
            uuid=uuid,
            date_created__gte=datetime.now() - timedelta(minutes=1)
        )
        return len(recent_scans) > 0