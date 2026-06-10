import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moba.settings")
django.setup()

from users.models import User, Profile
user = User.objects.get(username="lukas")
try:
    print("Profile exists:", user.profile is not None)
except Exception as e:
    print("Error accessing profile:", repr(e))
