from django.db import models

class Department(models.Model):
    department_name = models.CharField(max_length=100, blank=False, null=False)
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
    subject_name = models.CharField(max_length=100, blank=False, null=False)
    year = models.CharField(max_length=100, blank=True, null=True)
    semester = models.CharField(max_length=100, blank=True, null=True)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.subject_name

class Weekday(models.Model):
    Weekday = models.CharField(max_length=100, blank=False, null=False)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.Weekday

class Employee(models.Model):
    employee_ID = models.CharField(max_length=100, blank=False, null=False)
    name = models.CharField(max_length=100, blank=False, null=False)
    position = models.ForeignKey(Employee_Position, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
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
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    time_in = models.DateTimeField(auto_now=False, auto_now_add=True)
    time_out = models.DateTimeField(null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.employee.name