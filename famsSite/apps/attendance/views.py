import pytz
import qrcode
import xlwt 
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Employee, Employee_DTR, Department, Schedule
from .forms import EmployeeForm, DepartmentForm, SubjectForm, ScheduleForm
from django.core.paginator import Paginator
from utils.camera_streaming_widget import CameraStreamingWidget
from datetime import datetime, date
from django.shortcuts import get_object_or_404

timezone = pytz.timezone('Asia/Manila')
date_today = datetime.now(timezone).strftime('%B %d, %Y %I:%M %p')

def Login_page(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('DTR_Export'))

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('DTR_Export'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            messages.error(request, 'Check your password!')
        
    return render(request, './admin/login_page.html')

@login_required(login_url=reverse_lazy("Login_page"))
def User_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('Login_page'))

@login_required(login_url=reverse_lazy("Login_page"))
def Admin_dashboard(request):
    employees = Employee.objects.all().count()
    departments = Department.objects.all().count()
    schedules = Schedule.objects.all().count()
    ctx = {
        'date_today': date_today,
        'employees': employees,
        'departments': departments,
        'schedules': schedules
    }
    return render(request, './admin/dashboard.html', ctx)

@login_required(login_url=reverse_lazy("Login_page"))
def HomePage(request):
    return redirect('QRPage')

def QRPage(request):

    try:
        if request.method == 'POST':
            qr_code_content = request.POST.get('qr_code_content')
            emp = Employee.objects.get(employee_ID=str(qr_code_content))
            uuid = request.GET.get('uuid')

            if Employee_DTR.is_duplicate(uuid):
                return render(request, 'duplicate_scan.html')
            else:
                if emp.status == 'out':
                    timezone = pytz.timezone('Asia/Manila')
                    emp_dtr = Employee_DTR.objects.create(
                        employee=emp,
                        status='ongoing',
                        weekday=datetime.now(timezone).strftime('%A')
                    )
                    emp.status = 'in'
                    emp_dtr.save()
                    emp.save()

                else:
                    emp_dtr = Employee_DTR.objects.all()
                    dtr = emp_dtr.get(employee = emp.id, status = "ongoing")

                    dtr.status = 'done'
                    timezone = pytz.timezone('Asia/Manila')
                    dtr.time_out = datetime.now(timezone)
                    emp.status = 'out'

                    time_in = dtr.time_in
                    time_out = dtr.time_out
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

                    dtr.total_working_hours = total_hours
                    dtr.save()
                    emp.save()
    except:
        return render(request, './attendance/error.html')
        
    return render(request, './attendance/qr.html')

@login_required(login_url=reverse_lazy("Login_page"))
def QRSuccessPage(request):
    return render(request, './attendance/qr_success.html')

@login_required(login_url=reverse_lazy("Login_page"))
def DTR_Export(request):
    employee_records = Employee_DTR.objects.all().order_by('-date_created') 
    paginator = Paginator(employee_records, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    records_count = len(employee_records)
    
    if request.method == 'POST':
        if 'export_dtr' in request.POST:
            DateFrom = request.POST.get('dateFrom')
            DateTo = request.POST.get('dateTo')
            
            queryset = Employee_DTR.objects.filter(date_in__range=[DateFrom, DateTo]).order_by('-date_in')

            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="Employee\'s DTR.xls"'

            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('Employee\'s DTR')
            ws.col(0).width  = 4000
            ws.col(1).width  = 8000
            ws.col(2).width  = 4000
            ws.col(3).width  = 8000
            ws.col(4).width  = 8000
            ws.col(5).width  = 4000

            # Sheet header, first row
            row_num = 0

            font_style = xlwt.XFStyle()
            font_style.font.bold = True

            columns = ['employee id', 'name', 'weekday', 'in', 'out', 'total hours']

            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)

            # Sheet body, remaining rows
            font_style = xlwt.XFStyle()

            rows = queryset.values_list('employee__employee_ID', 'employee__name', 'weekday', 'time_in', 'time_out', 'total_working_hours')
            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    if isinstance(row[col_num], date):
                        dateCol = row[col_num].strftime('%B %d, %Y %I:%M %p')
                        ws.write(row_num, col_num, dateCol, font_style)
                    else:
                        ws.write(row_num, col_num, row[col_num], font_style)

            wb.save(response)
            return response
    
    ctx ={
        'page_obj': page_obj,
        'records_count': records_count
    }
    return render(request, './admin/dtr_export.html', ctx)

@login_required(login_url=reverse_lazy("Login_page"))
def Add_Employee_Page(request):
    form = EmployeeForm

    if request.method == "POST":
        empForm = EmployeeForm(request.POST)
        if empForm.is_valid():
            emp = empForm.save(commit=False)
            name = empForm.cleaned_data.get('name')
            emp.save()
            messages.success(request, '{} employee successfully created'.format(name))
            return HttpResponseRedirect(reverse('Add_Employee_Page'))
            
        else:
            messages.error(request, form.errors)
    ctx = {
        'form' : form,
        'date_today': date_today
    }
    return render(request, './admin/add_employee.html',ctx)

@login_required(login_url=reverse_lazy("Login_page"))
def Add_Department_Page(request):
    form = DepartmentForm

    if request.method == "POST":
        deptForm = DepartmentForm(request.POST)
        if deptForm.is_valid():
            dept = deptForm.save(commit=False)
            name = deptForm.cleaned_data.get('department_name')
            dept.save()
            messages.success(request, '{} Department successfully created'.format(name))
            return HttpResponseRedirect(reverse('Add_Department_Page'))
            
        else:
            messages.error(request, form.errors)
    ctx = {
        'form' : form,
        'date_today': date_today
    }
    return render(request, './admin/add_department.html',ctx)

@login_required(login_url=reverse_lazy("Login_page"))
def Add_Subject_Page(request):
    form = SubjectForm

    if request.method == "POST":
        subjForm = SubjectForm(request.POST)
        if subjForm.is_valid():
            subj = subjForm.save(commit=False)
            name = subjForm.cleaned_data.get('subject_name')
            subj.save()
            messages.success(request, '{} employee successfully created'.format(name))
            return HttpResponseRedirect(reverse('Add_Subject_Page'))
            
        else:
            messages.error(request, form.errors)

    ctx = {
        'form' : form,
        'date_today': date_today
    }
    return render(request, './admin/add_subject.html',ctx)

@login_required(login_url=reverse_lazy("Login_page"))
def Add_Schedule_Page(request):
    form = ScheduleForm

    if request.method == "POST":
        schedForm = ScheduleForm(request.POST)
        if schedForm.is_valid():
            sched = schedForm.save(commit=False)
            sched.save()
            messages.success(request, 'Sched successfully created')
            return HttpResponseRedirect(reverse('Add_Schedule_Page'))
            
        else:
            messages.error(request, form.errors)

    ctx = {
        'form' : form,
        'date_today': date_today
    }
    return render(request, './admin/add_Schedule.html',ctx)

@login_required(login_url=reverse_lazy("Login_page"))
def Employee_list(request):
    emps = Employee.objects.all().order_by('-date_created')
    paginator = Paginator(emps, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    emps_count = len(emps)
    ctx = {
        'date_today': date_today,
        'emps': emps,
        'emps_count': emps_count,
        'page_obj': page_obj
    }
    return render(request, './admin/employees.html', ctx)

@login_required(login_url=reverse_lazy("Login_page"))
def Employee_page(request, pk):
    emp = get_object_or_404(Employee, pk=pk)
    scheds = emp.schedule_set.all().order_by('-date_created')
    dtrs = emp.employee_dtr_set.all().order_by('-date_created')
    
    if request.method == 'POST':
        if 'export_dtr' in request.POST:
            DateFrom = request.POST.get('dateFrom')
            DateTo = request.POST.get('dateTo')
            
            queryset = dtrs.filter(date_in__range=[DateFrom, DateTo]).order_by('-date_in')

            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="{}\'s DTR.xls"'.format(emp.name)

            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet(emp.name + '\'s DTR')
            ws.col(0).width  = 4000
            ws.col(1).width  = 8000
            ws.col(2).width  = 4000
            ws.col(3).width  = 8000
            ws.col(4).width  = 8000
            ws.col(5).width  = 4000

            # Sheet header, first row
            row_num = 0

            font_style = xlwt.XFStyle()
            font_style.font.bold = True

            columns = ['employee id', 'name', 'weekday', 'in', 'out', 'total hours']

            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)

            # Sheet body, remaining rows
            font_style = xlwt.XFStyle()

            rows = queryset.values_list('employee__employee_ID', 'employee__name', 'weekday', 'time_in', 'time_out', 'total_working_hours')
            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    if isinstance(row[col_num], date):
                        dateCol = row[col_num].strftime('%B %d, %Y %I:%M %p')
                        ws.write(row_num, col_num, dateCol, font_style)
                    else:
                        ws.write(row_num, col_num, row[col_num], font_style)

            wb.save(response)
            return response    

    paginator = Paginator(scheds, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    scheds_count = len(scheds)

    ctx = {
        'emp': emp,
        'scheds': scheds,
        'page_obj': page_obj,
        'scheds_count': scheds_count
    }
    return render(request, 'employee/employee_details.html', ctx)

@login_required(login_url=reverse_lazy("Login_page"))
def Department_list(request):
    depts = Department.objects.all()
    paginator = Paginator(depts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    depts_count = len(depts)
    ctx = {
        'date_today': date_today,
        'depts': depts,
        'depts_count': depts_count,
        'page_obj': page_obj
    }
    return render(request, './admin/departments.html', ctx)

@login_required(login_url=reverse_lazy("Login_page"))
def Generate_QR_page(request):
    if request.method == 'POST':
        if 'generate_qr' in request.POST:
            data = request.POST.get('qr_url')
            qr = qrcode.QRCode(version=1, box_size=30, border=2)
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Render the QR code image in your template
            response = HttpResponse(content_type='image/png')
            response['Content-Disposition'] = 'attachment; filename="{}_QRCode.png"'.format(data)
            img.save(response, 'PNG')
            return response
    else:
        # Render the form in your template
        return render(request, './attendance/generate_qr.html')

    stream = CameraStreamingWidget()
    success, frame = stream.camera.read()
    if success:
        status = True
    else:
        status = False
    return render(request, 'detect_barcodes/detect.html', context={'cam_status': status})

    