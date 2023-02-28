from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePage, name="HomePage"),
    path('qr', views.QRPage, name="QRPage"),
    path('QRSuccess', views.QRSuccessPage, name="QRSuccessPage"),
    path('login', views.Login_page, name="Login_page"),
    path('l0g0u7', views.User_logout, name="User_logout"),
    path('dashboard', views.Admin_dashboard, name="Admin_dashboard"),

    path('dtr/export', views.DTR_Export, name="DTR_Export"),
    
    # path('', views.detect, name='detect_barcodes'),
    # path('camera_feed', views.camera_feed, name='camera_feed'),
]
