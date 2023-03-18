from django import forms
from .models import Employee, Department, Schedule, Subject

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = {'employee_ID', 'name', 'position', 'department', 'employee_status'}
        widgets = {
            'employee_ID': forms.TextInput(attrs={
                'placeholder': 'Employee ID',
                'class': 'rounded-md',
                'required': True,
            }),
            'name': forms.TextInput(attrs={
                'placeholder': 'Name',
                'class': 'rounded-md',
                'required': True,
            }),
            'position': forms.Select(attrs={
                'placeholder': 'Position',
                'class': 'rounded-md',
                'required': True,
            }),
            'department': forms.Select(attrs={
                'class': 'rounded-md',
                'required': True,
            }),
            'employee_status': forms.Select(attrs={
                'class': 'rounded-md',
                'required': True,
            }),
        }

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = {'department_name', 'address', 'room_no', 'floor'}
        widgets = {
            'department_name': forms.TextInput(attrs={
                'placeholder': 'Department name',
                'class': 'rounded-md',
                'required': True
            }),
            'address': forms.TextInput(attrs={
                'placeholder': 'Address',
                'class': 'rounded-md',
                'required': True
            }),
            'room_no': forms.TextInput(attrs={
                'placeholder': 'Room number',
                'class': 'rounded-md',
                'required': True
            }),
            'floor': forms.TextInput(attrs={
                'placeholder': 'Floor level',
                'class': 'rounded-md',
                'required': True
            }),
        }

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = {'subject_code', 'subject_name', 'year', 'semester'}
        widgets = {
            'subject_code': forms.TextInput(attrs={
                'placeholder': 'Subject Code',
                'class': 'rounded-md',
                'required': True
            }),
            'subject_name': forms.TextInput(attrs={
                'placeholder': 'Subject name',
                'class': 'rounded-md',
                'required': True
            }),
            'year': forms.TextInput(attrs={
                'placeholder': 'Year level',
                'class': 'rounded-md',
                'required': True
            }),
            'semester': forms.NumberInput(attrs={
                'placeholder': 'Semester',
                'class': 'rounded-md',
                'required': True
            }),
        }

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = {'employee', 'subject', 'weekday', 'time_in', 'time_out'}
        widgets = {
            'employee': forms.Select(attrs={
                'class': 'rounded-md',
                'required': True
            }),
            'subject': forms.Select(attrs={
                'class': 'rounded-md',
                'required': True
            }),
            'weekday': forms.Select(attrs={
                'class': 'rounded-md',
                'required': True
            }),
            'time_in': forms.TimeInput(attrs={
                'class': 'rounded-md',
                'required': True,
            }),
            'time_out': forms.TimeInput(attrs={
                'class': 'rounded-md',
                'required': True
            }),
        }