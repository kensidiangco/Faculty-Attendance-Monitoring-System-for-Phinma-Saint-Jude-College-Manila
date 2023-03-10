from rest_framework import serializers
from .models import Employee_DTR, Employee

class Employee_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('employee_ID', 'name')

class Employee_DTR_Serializer(serializers.ModelSerializer):
    employee = Employee_Serializer(read_only=True)

    class Meta:
        model = Employee_DTR
        fields = ('id', 'uuid', 'employee', 'weekday', 'time_in', 'time_out', 'total_working_hours')
