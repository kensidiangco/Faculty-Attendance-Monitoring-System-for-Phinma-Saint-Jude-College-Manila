import json
import qrcode
import pytz
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Employee, Employee_DTR, Department, Schedule
from .forms import EmployeeForm, DepartmentForm, SubjectForm, ScheduleForm
from django.core.paginator import Paginator
from datetime import datetime, time, date, timedelta
from django.shortcuts import get_object_or_404
from .utils import export_attendance_excel, Time_in_sched, Time_out_sched, Pagination_feature

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
        'employees': employees,
        'departments': departments,
        'schedules': schedules
    }
    return render(request, './admin/dashboard.html', ctx)

@login_required(login_url=reverse_lazy("Login_page"))
def HomePage(request):
    return redirect('DTR_Export')

def QRPage(request):
    if request.method == 'POST':
        qr_code_content = request.POST.get('qr_code_content')
        try:
            data = json.loads(qr_code_content)
            emp = Employee.objects.get(employee_ID=str(data['employee_id']).upper())

            if emp.working_status == "INACTIVE":
                raise KeyError
            
            # Check if professor is out if true then proceed to time in else time out
            if emp.status == 'OUT' or emp.status == 'out':
                # Check if professor has schedule today.
                manila_tz = pytz.timezone('Asia/Manila')
                current_time = timezone.now().astimezone(manila_tz)
                half_hour_ago = current_time - timedelta(minutes=30)
                one_hour_later = current_time + timedelta(hours=1)

                sched = emp.schedule_set.all().filter(time_in__range=[half_hour_ago, one_hour_later], status="VACANT").order_by('time_in')
                
                if sched:
                    # Check if sched is valid
                    expiration = datetime.strptime(str(sched.last().expiration_date), '%Y-%m-%d')
                    current_date = date.today()
                    if current_date > expiration.date():
                        raise KeyError 

                    if str(sched.last().weekday).upper() == datetime.now().strftime('%A').upper():
                        Time_in_sched(sched, emp)
                        return HttpResponseRedirect(reverse('DTR_Export'))
                    else:
                        raise ValueError
                else:
                    raise ValueError
            
            else:
                emp_dtr = Employee_DTR.objects.all()
                Time_out_sched(emp_dtr, emp)
                return HttpResponseRedirect(reverse('DTR_Export'))

        except ValueError:
            return render(request, './attendance/error/error_attendance.html')

        except KeyError:
            print("INVALID QR CODE")
            return render(request, './attendance/error/expired_schedule.html')

        except:
            print("ERROR")
            return render(request, './attendance/error/error_attendance.html')
            
    return render(request, './attendance/qr.html')

@login_required(login_url=reverse_lazy("Login_page"))
def QRSuccessPage(request):
    return render(request, './attendance/qr_success.html')

@login_required(login_url=reverse_lazy("Login_page"))
def DTR_Export(request):

    employee_records = Employee_DTR.objects.all().order_by('-date_in') 
    current_date = datetime.now()
    SY_now = employee_records.filter(date_created__range=[datetime(current_date.year, 1, 1), datetime(current_date.year, 12, 31)])

    page_obj = Pagination_feature(request, SY_now, 8)
    records_count = len(SY_now)

    if request.method == 'POST':
        if 'export_dtr' in request.POST:
            DateFrom = request.POST.get('dateFrom')
            DateTo = request.POST.get('dateTo')
            queryset = Employee_DTR.objects.filter(date_in__range=[DateFrom, DateTo]).order_by('-date_in')

            return export_attendance_excel('EMPLOYEE', queryset)    
 
    ctx ={
        'page_obj': page_obj,
        'records_count': records_count,
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
            messages.success(request, '{} employee successfully created'.format(name).upper())
            return HttpResponseRedirect(reverse('Employee_page', kwargs={'pk': emp.id}))
            
        else:
            emp_id = empForm.cleaned_data.get('employeeID')
            messages.error(request, "Employee ID must be unique.")
    ctx = {
        'form' : form,
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
            messages.error(request, 'Department name must be unique (Do not double click the submit button!)')
    ctx = {
        'form' : form,
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
            messages.success(request, '{} SUBJECT SUCCESSFULLY CREATED'.format(name).upper())
            return HttpResponseRedirect(reverse('Add_Subject_Page'))
            
        else:
            messages.error(request, form.errors)

    ctx = {
        'form' : form,
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
            messages.success(request, '{} Sched for {} successfully created'.format(sched.subject.subject_name, sched.employee.name).upper())
            return HttpResponseRedirect(reverse('Employee_page', kwargs={'pk':sched.employee.id}))
            
        else:
            messages.error(request, form.errors)

    ctx = {
        'form' : form,
    }
    return render(request, './admin/add_schedule.html',ctx)

@login_required(login_url=reverse_lazy("Login_page"))
def Employee_list(request):
    emps = Employee.objects.all().order_by('-date_created')
    page_obj = Pagination_feature(request, emps, 5)
    emps_count = len(emps)

    ctx = {
        'emps': emps,
        'emps_count': emps_count,
        'page_obj': page_obj
    }

    return render(request, './admin/employees.html', ctx)

@login_required(login_url=reverse_lazy("Login_page"))
def Employee_page(request, pk):
    emp = get_object_or_404(Employee, pk=pk)
    scheds = emp.schedule_set.all().order_by('time_in')
    dtrs = emp.employee_dtr_set.all().order_by('-date_created')

    if request.method == 'POST':
        if 'export_dtr' in request.POST:
            DateFrom = request.POST.get('dateFrom')
            DateTo = request.POST.get('dateTo')
            queryset = dtrs.filter(date_in__range=[DateFrom, DateTo]).order_by('-date_in')
            return export_attendance_excel(emp.name, queryset)    

    page_obj = Pagination_feature(request, scheds, 5)
    scheds_count = len(scheds)

    late_count = dtrs.filter(attendance_status="LATE").count()
    not_late_count = dtrs.filter(attendance_status="NOT LATE").count()

    ctx = {
        'emp': emp,
        'scheds': scheds,
        'page_obj': page_obj,
        'scheds_count': scheds_count,
        'late_count': late_count,
        'not_late_count': not_late_count,
    }
    
    return render(request, 'employee/employee_details.html', ctx)

@login_required(login_url=reverse_lazy("Login_page"))
def Department_list(request):
    depts = Department.objects.all().order_by('-department_name')
    page_obj = Pagination_feature(request, depts, 5)
    depts_count = len(depts)

    ctx = {
        'depts': depts,
        'depts_count': depts_count,
        'page_obj': page_obj
    }

    return render(request, './admin/departments.html', ctx)

@login_required(login_url=reverse_lazy("Login_page"))
def Department_page(request, pk):
    department = get_object_or_404(Department, pk=pk)

    response_data = {
        'id': department.id,
        'name': department.department_name,
        'employee': department.employee_set.all
    }
    
    return JsonResponse(response_data)

@login_required(login_url=reverse_lazy("Login_page"))
def Generate_QR_page(request):
    if request.method == 'POST':
        if 'generate_qr' in request.POST:
            employee_id = request.POST.get('employee_id')
            expiration = request.POST.get('expiration')

            data = {
                'expiration': expiration,
                'employee_id': employee_id
            }
            
            # Parse data using json
            json_data = json.dumps(data)
            qr = qrcode.QRCode(version=12, box_size=30, border=2, error_correction=qrcode.constants.ERROR_CORRECT_L)
            qr.add_data(json_data)
            qr.make(fit=True)

            # Save qr image
            img = qr.make_image(fill_color="black", back_color="white")
            # buffer = BytesIO()
            # # img.save(buffer)
            # response = HttpResponse(buffer.getvalue(), content_type='image/png')
            # response['Content-Disposition'] = 'inline; filename="qr.png"'
            # response['Content-Length'] = str(len(buffer.getvalue()))
            # response['target'] = '_blank'

            response = HttpResponse(content_type='image/png')
            response['Content-Disposition'] = 'attachment; filename="{}_QRCode.png"'.format(employee_id)
            img.save(response, 'PNG')
            return response
    else:
        # Render the form in your template
        return render(request, './attendance/generate_qr.html')