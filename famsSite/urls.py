from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .apps.attendance.management.commands import runapscheduler

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('famsSite.apps.attendance.urls')),
    path("accounts/", include("django.contrib.auth.urls")),
    path("select2/", include("django_select2.urls")),
    path("__reload__/", include("django_browser_reload.urls")),
]

if settings.DEBUG: 
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)