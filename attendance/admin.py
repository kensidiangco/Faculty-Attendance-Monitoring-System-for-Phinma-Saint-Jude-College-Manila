from django.contrib import admin
from .models import Employee, Employee_DTR, Subject, Schedule, Department, Employee_Absence_Record

admin.site.register(Employee)
admin.site.register(Employee_DTR)
admin.site.register(Schedule)
admin.site.register(Subject)
admin.site.register(Department)
admin.site.register(Employee_Absence_Record)