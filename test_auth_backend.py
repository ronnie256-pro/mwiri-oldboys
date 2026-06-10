import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moba.settings")

from django.conf import settings
settings.DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': settings.BASE_DIR / 'db.sqlite3',
    }
}

django.setup()

from django.test import RequestFactory
from users.backends import CaseInsensitiveModelBackend

backend = CaseInsensitiveModelBackend()
request = RequestFactory().post('/accounts/login/')

print("Testing missing user")
try:
    user = backend.authenticate(request, username="doesnotexist", password="wrongpassword")
    print("Result:", user)
except Exception as e:
    print("Error:", type(e), e)

print("Testing existing user wrong password")
try:
    user = backend.authenticate(request, username="testuser123", password="wrongpassword")
    print("Result:", user)
except Exception as e:
    print("Error:", type(e), e)

