# runserver.py
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DataEngineeringConcepts.settings')

from django.core.management import execute_from_command_line

if __name__ == '__main__':
    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])

