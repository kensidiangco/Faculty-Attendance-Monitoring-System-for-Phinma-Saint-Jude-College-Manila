from django.apps import AppConfig


class AttendanceConfig(AppConfig):
    name = 'attendance'

    # def ready(self):
    #     from jobs import updater
    #     updater.start_jobs()
