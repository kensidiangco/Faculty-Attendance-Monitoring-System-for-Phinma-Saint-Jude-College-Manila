from django import forms
from .models import Employee, Department, Schedule, Subject
from django_select2 import forms as s2forms

class EmployeeWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "name__icontains",
    ]

class SubjectWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "subject_code__icontains",
        "subject_name__icontains",
    ]

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = {'employee_ID', 'name', 'position', 'department', 'employee_status'}
        widgets = {
            'employee_ID': forms.TextInput(attrs={
                'placeholder': 'Employee ID',
                'class': 'rounded-md p-2',
                'oninput': 'this.value = this.value.toUpperCase()',
                'autofocus': True,
                'required': True,
            }),
            'name': forms.TextInput(attrs={
                'placeholder': 'Name',
                'class': 'rounded-md p-2',
                'required': True,
                'oninput': 'this.value = this.value.toUpperCase()',
            }),
            'position': forms.Select(attrs={
                'placeholder': 'Position',
                'class': 'rounded-md p-2',
                'required': True,
            }),
            'department': forms.Select(attrs={
                'class': 'rounded-md p-2',
                'required': True,
            }),
            'employee_status': forms.Select(attrs={
                'class': 'rounded-md p-2',
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
                'class': 'rounded-md p-2',
                'oninput': 'this.value = this.value.toUpperCase()',
                'autofocus': True,
                'required': True,
            }),
            'address': forms.TextInput(attrs={
                'placeholder': 'Address',
                'class': 'rounded-md p-2',
                'oninput': 'this.value = this.value.toUpperCase()',
                'required': True
            }),
            'room_no': forms.NumberInput(attrs={
                'placeholder': 'Room number',
                'class': 'rounded-md p-2',
                'required': True
            }),
            'floor': forms.NumberInput(attrs={
                'placeholder': 'Floor level',
                'class': 'rounded-md p-2',
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
                'class': 'rounded-md p-2',
                'oninput': 'this.value = this.value.toUpperCase()',
                'autofocus': True,
                'required': True,
            }),
            'subject_name': forms.TextInput(attrs={
                'placeholder': 'Subject name',
                'class': 'rounded-md p-2',
                'oninput': 'this.value = this.value.toUpperCase()',
                'required': True
            }),
            'year': forms.NumberInput(attrs={
                'placeholder': 'Year level',
                'class': 'rounded-md p-2',
                'oninput': 'this.value = this.value.toUpperCase()',
                'required': True
            }),
            'semester': forms.NumberInput(attrs={
                'placeholder': 'Semester',
                'class': 'rounded-md p-2',
                'required': True
            }),
        }

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = {'employee', 'subject', 'weekday', 'time_in', 'time_out', 'expiration_date'}
        widgets = {
            'employee': EmployeeWidget(attrs={
                'class': 'rounded-md p-2',
                'required': True
            }),
            'subject': SubjectWidget(attrs={
                'class': 'rounded-md p-2',
                'required': True
            }),
            'weekday': forms.Select(attrs={
                'class': 'rounded-md p-2',
                'required': True
            }),
            'time_in': forms.TimeInput(attrs={
                'class': 'rounded-md p-2',
                'type': 'time',
                'required': True,
            }),
            'time_out': forms.TimeInput(attrs={
                'class': 'rounded-md p-2',
                'type': 'time',
                'required': True
            }),
            'expiration_date': forms.DateInput(attrs={
                'class': 'rounded-md p-2',
                'name': 'expiration',
                'type': 'date',
                'required': True,
            }),
        }