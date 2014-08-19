"""
WSGI config for otaupdate project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys

path = '/home/nexell/otaupdate-server'
if path not in sys.path:
    sys.path.append(path)


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "otaupdate.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
