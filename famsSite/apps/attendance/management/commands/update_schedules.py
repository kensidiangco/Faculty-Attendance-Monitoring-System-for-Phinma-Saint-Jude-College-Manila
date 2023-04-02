from django.core.management.base import BaseCommand
from ...models import Schedule

class Command(BaseCommand):
    help = 'Updates the status attribute of all Schedule objects'

    def handle(self, *args, **options):
        schedules = Schedule.objects.all()
        for schedule in schedules:
            schedule.status = 'VACANT'
            schedule.save()

        self.stdout.write(self.style.SUCCESS('SCHEDULE STATUS SUCCESSFULLY UPDATED!'))