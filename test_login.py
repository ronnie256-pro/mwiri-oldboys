import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moba.settings")
django.setup()

from django.test import Client
from users.models import User

client = Client()
user = User.objects.get(username="lukas")
client.force_login(user)

response = client.get('/accounts/my-account/')
print("Status code:", response.status_code)
if response.status_code != 200:
    print("Content:", response.content.decode()[:500])
