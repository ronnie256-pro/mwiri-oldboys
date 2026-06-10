import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moba.settings")

from django.conf import settings
settings.DATABASES['default'] = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'postgres',
    'USER': 'postgres',
    'PASSWORD': '*@ronnie2026#',
    'HOST': 'localhost',
    'PORT': '5432',
}

django.setup()
from django.db import connection
try:
    connection.ensure_connection()
    print("Django connected to postgres successfully!")
except Exception as e:
    print("Django connection failed:", e)
