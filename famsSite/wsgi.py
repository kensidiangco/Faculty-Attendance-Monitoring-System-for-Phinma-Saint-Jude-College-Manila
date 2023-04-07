import os
import subprocess
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'famsSite.settings')

application = get_wsgi_application()
subprocess.call(['python', 'manage.py', 'runapscheduler'])