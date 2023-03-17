from django.urls import path
from . import views
from .serializerViews import Employee_DTR_SerializerList, Employee_DTR_SerializerDetail

urlpatterns = [
    path('', views.HomePage, name="HomePage"),
    path('qr', views.QRPage, name="QRPage"),
    path('QRSuccess', views.QRSuccessPage, name="QRSuccessPage"),
    path('login', views.Login_page, name="Login_page"),
    path('l0g0u7', views.User_logout, name="User_logout"),
    path('dashboard', views.Admin_dashboard, name="Admin_dashboard"),
    path('create/employee', views.Add_Employee_Page, name="Add_Employee_Page"),
    path('create/department', views.Add_Department_Page, name="Add_Department_Page"),
    path('create/schedule', views.Add_Schedule_Page, name="Add_Schedule_Page"),
    path('create/subject', views.Add_Subject_Page, name="Add_Subject_Page"),
    path('employees', views.Employee_list, name="Employee_list"),
    path('emplopyee/<int:pk>', views.Employee_page, name="Employee_page"),
    path('departments', views.Department_list, name="Department_list"),
    path('generate', views.Generate_QR_page, name="Generate_QR_page"),
    path('dtr/export', views.DTR_Export, name="DTR_Export"),
    
    # API VIEWS
    path('api/records/', Employee_DTR_SerializerList.as_view()),
    path('api/records/<int:pk>/', Employee_DTR_SerializerDetail.as_view()),

    # path('', views.detect, name='detect_barcodes'),
    # path('camera_feed', views.camera_feed, name='camera_feed'),
]
