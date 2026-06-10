import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moba.settings")

from django.conf import settings
settings.DEBUG = False
settings.ALLOWED_HOSTS = ['testserver']

# Force SQLite for the test
settings.DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': settings.BASE_DIR / 'db.sqlite3',
    }
}

django.setup()

from django.test import Client
from users.models import User

client = Client(HTTP_HOST='testserver')
user = User.objects.get(username="testuser123")
client.force_login(user)

response = client.get('/accounts/my-account/')
print("Status:", response.status_code)
if response.status_code == 500:
    print(response.content.decode()[:1000])
