"""
WSGI config for Company project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Company.settings')

application = get_wsgi_application()
