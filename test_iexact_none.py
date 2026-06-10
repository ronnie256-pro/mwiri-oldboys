import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moba.settings")
django.setup()

from users.models import User
try:
    User.objects.filter(username__iexact=None)
    print("Filter succeeded")
except Exception as e:
    print("Filter failed:", type(e), e)
