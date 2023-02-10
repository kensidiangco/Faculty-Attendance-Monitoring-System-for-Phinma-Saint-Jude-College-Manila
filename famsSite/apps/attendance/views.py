from django.shortcuts import render, redirect
from .models import Employee

def HomePage(request):
    return render(request, './home.html')

def QRPage(request):
    if request.method == 'POST':
        qr_code_content = request.POST.get('qr_code_content')
        emp = Employee.objects.get(employee_ID=str(qr_code_content))
        print(emp.id)
        
    return render(request, './attendance/qr.html')

def QRSuccessPage(request):
    return render(request, './attendance/qr_success.html')