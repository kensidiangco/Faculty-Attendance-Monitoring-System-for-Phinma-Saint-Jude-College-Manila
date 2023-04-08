#!/usr/bin/env python
import os
import sys

# Set up the Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "famsSite.settings")
try:
    from django.core.management import execute_from_command_line
except ImportError:
    # The module is not installed, so install it
    print("Installing Django...")
    os.system("pip install django")
    from django.core.management import execute_from_command_line

# Apply database migrations
execute_from_command_line(["manage.py", "runapscheduler"])