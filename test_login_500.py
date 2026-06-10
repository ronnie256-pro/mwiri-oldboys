import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moba.settings")
django.setup()

from django.test import Client

client = Client()
resp = client.post('/accounts/login/', {'username': 'testuser123', 'password': 'somepassword'})
print("Login status:", resp.status_code)
if resp.status_code == 500:
    print(resp.content.decode()[:1000])

