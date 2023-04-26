import xlwt 
import pytz
from datetime import date
from django.http import HttpResponse
from .models import Employee_DTR, Schedule
from datetime import datetime, time
from django.core.paginator import Paginator

timezone = pytz.timezone('Asia/Manila')

def Pagination_feature(request, item, page):
    paginator = Paginator(item, page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj

def Time_in_sched(sched, emp):
    # Getting time difference of time today and time in sched to determine if employee is late
    dt = datetime.now()
    time_in_sched = sched.time_in
    dt_and_time_in_sched = datetime.combine(dt.date(), time_in_sched)
    time_diff = dt - dt_and_time_in_sched

    # If late
    if time_diff.total_seconds() > 0:
        emp_dtr = Employee_DTR.objects.create(
            employee=emp,
            schedule=sched,
            status='ONGOING',
            weekday=datetime.now(timezone).strftime('%A'),
            time_in=datetime.now(timezone),
            attendance_status = 'LATE'
        )
    # If not late
    if time_diff.total_seconds() < 0:
        emp_dtr = Employee_DTR.objects.create(
            employee=emp,
            schedule=sched,
            status='ONGOING',
            weekday=datetime.now(timezone).strftime('%A'),
            time_in=datetime.now(timezone),
            attendance_status = 'NOT LATE'
        )
    # Change the status for tracking the data
    emp.status = 'IN'
    schd = Schedule.objects.get(id = sched.id)
    schd.status = 'ONGOING'

    # Save all the changes
    emp_dtr.save()
    schd.save()
    emp.save()

def Time_out_sched(emp_dtr, emp):
    dtr = emp_dtr.get(employee=emp.id, status="ONGOING")
    sched = emp.schedule_set.all().filter(employee=emp.id, status="ONGOING").order_by('time_in')
    dtr.status = 'DONE'
    timezone = pytz.timezone('Asia/Manila')
    dtr.time_out = datetime.now(timezone)

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
    schd = Schedule.objects.get(id = sched.last().id)
    schd.status = 'DONE'
    emp.status = 'OUT'

    dtr.save() 
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
    ws.col(3).width  = 4000
    ws.col(4).width  = 4000
    ws.col(5).width  = 4000
    ws.col(6).width  = 4000

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['employee id', 'name', 'date', 'weekday', 'in', 'out', 'total hours']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = queryset.values_list('employee__employee_ID', 'employee__name', 'date_in', 'weekday', 'time_in__time', 'time_out__time', 'total_working_hours')
    
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if isinstance(row[col_num], date):
                dateCol = row[col_num].strftime('%B %d, %Y')
                ws.write(row_num, col_num, dateCol, font_style)
            elif isinstance(row[col_num], time):
                timeCol = row[col_num].strftime('%I:%M %p')
                ws.write(row_num, col_num, timeCol, font_style)
            else:
                ws.write(row_num, col_num, row[col_num], font_style)
            

    wb.save(response)
    return response