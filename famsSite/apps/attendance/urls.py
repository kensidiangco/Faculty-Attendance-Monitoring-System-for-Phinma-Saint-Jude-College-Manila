from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePage, name="HomePage"),
    path('qr', views.QRPage, name="QRPage"),
    path('QRSuccess', views.QRSuccessPage, name="QRSuccessPage"),
]
