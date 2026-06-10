import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moba.settings")
django.setup()

from users.forms import RegistrationForm

data = {
    'username': 'Ronnie4',
    'password1': 'Ronnie123!',
    'password2': 'Ronnie123!',
    'first_name': 'Ronnie',
    'last_name': 'Test',
    'email': 'ronnie4@test.com',
    'phone_number': '1234567890',
}
form = RegistrationForm(data)
print("Is valid?", form.is_valid())
if not form.is_valid():
    print("Errors:", form.errors)
