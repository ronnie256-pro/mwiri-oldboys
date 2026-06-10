import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moba.settings")
django.setup()

from users.models import User
for user in User.objects.order_by('-id')[:2]:
    print(f"Username: {user.username}, is_active: {user.is_active}, password: {user.password[:20]}...")
