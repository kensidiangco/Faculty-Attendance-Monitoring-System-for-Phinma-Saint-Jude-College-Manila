import xlwt 
from datetime import date
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Employee_DTR, Schedule
from datetime import datetime, time
import pytz

def time_in_schedule(request, emp):
    timezone = pytz.timezone('Asia/Manila')
    hr_in = int(datetime.now().strftime('%H'))
    emp_in = time(hour=hr_in - 1, minute=30, second=0)
    emp_in_later = time(hour=hr_in + 1, minute=0, second=0)
    sched = emp.schedule_set.all().filter(time_in__range=(emp_in, emp_in_later), status="VACANT").order_by('time_in')
    
    # Check if professor has schedule today.
    try:
        if str(sched[len(sched)-1].weekday) != datetime.now().strftime('%A'):
            raise ValueError("You have no sched today!.")
    except:
        return render(request, './attendance/duplicate_attendance.html')

        
    dt = datetime.now()
    t = sched[len(sched)-1].time_in
    dt_t = datetime.combine(dt.date(), t)
    time_diff = dt - dt_t

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

    if time_diff.total_seconds() > 0:
        emp_dtr = Employee_DTR.objects.create(
            employee=emp,
            status='ongoing',
            weekday=datetime.now(timezone).strftime('%A'),
            time_in=datetime.now(timezone),
            attendance_status = 'LATE'
        )
        
    if time_diff.total_seconds() < 0:
        emp_dtr = Employee_DTR.objects.create(
            employee=emp,
            status='ongoing',
            weekday=datetime.now(timezone).strftime('%A'),
            time_in=datetime.now(timezone),
            attendance_status = 'NOT LATE'
        )

    emp_dtr.save()
    emp.status = 'in'
    schd = Schedule.objects.get(id = sched[len(sched)-1].id)
    schd = 'ONGOING'
    emp.save()

def time_out_schedule(request, emp):
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
    sched = emp.schedule_set.all().filter(status="VACANT").order_by('time_in')
    schd = Schedule.objects.get(id = sched[len(sched)-1].id)
    schd.status = 'DONE'
    schd.save()
    
    emp.save()

def export_attendance_excel(name, queryset):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="{}\'s DTR.xls"'.format(name)

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(name + '\'s DTR')
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
    print("working")
    return response