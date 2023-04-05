from rest_framework import serializers
from .models import Employee_DTR, Employee, Department

class Employee_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('employee_ID', 'name', 'position')

class Employee_DTR_Serializer(serializers.ModelSerializer):
    employee = Employee_Serializer(read_only=True)

    class Meta:
        model = Employee_DTR
        fields = ('id', 'uuid', 'employee', 'weekday', 'time_in', 'time_out', 'total_working_hours')

class Department_Serializer(serializers.ModelSerializer):
    employees = serializers.SerializerMethodField()
    class Meta:
        model = Department
        fields = ('id', 'department_name', 'employees')

    def get_employees(self, obj):
        emps = Employee.objects.filter(department=obj)
        return Employee_Serializer(emps, many=True).data
