from django.contrib import admin
from .models import Employee, Employee_Position, Employee_DTR, Subject, Schedule, Weekday, Department

admin.site.register(Employee)
admin.site.register(Employee_Position)
admin.site.register(Employee_DTR)
admin.site.register(Schedule)
admin.site.register(Subject)
admin.site.register(Weekday)
admin.site.register(Department)