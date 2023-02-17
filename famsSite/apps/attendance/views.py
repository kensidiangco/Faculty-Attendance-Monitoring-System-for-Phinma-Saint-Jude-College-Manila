from django.shortcuts import render, redirect
from .models import Employee, Employee_DTR

import datetime

def HomePage(request):
    return render(request, './home.html')

def QRPage(request):
    if request.method == 'POST':
        qr_code_content = request.POST.get('qr_code_content')
        emp = Employee.objects.get(employee_ID=str(qr_code_content))
        print(emp.status)

        if emp.status == 'out':
            emp_dtr = Employee_DTR.objects.create(
                employee=emp,
                status='ongoing'
            )
            emp.status = 'in'
            
            emp_dtr.save()
            emp.save()

        else:
            emp_dtr = Employee_DTR.objects.all()
            dtr = emp_dtr.get(employee = emp.id, status = "ongoing")

            dtr.status = 'done'
            dtr.time_out = datetime.datetime.now()
            emp.status = 'out'
            dtr.save()
            emp.save()
        
    return render(request, './attendance/qr.html')

def QRSuccessPage(request):
    return render(request, './attendance/qr_success.html')