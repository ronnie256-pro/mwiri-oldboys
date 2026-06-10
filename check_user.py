import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moba.settings")
django.setup()

from users.models import User
user = User.objects.last()
if user:
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")
    print(f"Is active: {user.is_active}")
    print(f"Has usable password: {user.has_usable_password()}")
    print(f"Role: {user.role}")
else:
    print("No users found.")
