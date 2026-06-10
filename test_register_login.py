import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moba.settings")
django.setup()

from django.test import Client
from users.models import User
from teaser.models import TeaserQuestion, Answer

client = Client()

questions = TeaserQuestion.objects.all()
teaser_data = {}
for q in questions:
    correct_ans = q.answers.filter(is_correct=True).first()
    if correct_ans:
        teaser_data[f'question_{q.id}'] = correct_ans.id

data = {
    'username': 'testuser123',
    'password1': 'StrongPass123!',
    'password2': 'StrongPass123!',
    'first_name': 'Test',
    'last_name': 'User',
    'email': 'test@example.com',
    'phone_number': '1234567890',
}
data.update(teaser_data)

# Submit registration
response = client.post('/accounts/register/', data)
print("Register response status:", response.status_code)
if response.status_code == 302:
    print("Redirect to:", response.url)
else:
    print("Register form errors:")
    print(response.context.get('form').errors if response.context.get('form') else "No form errors")

# Try login
login_response = client.post('/accounts/login/', {
    'username': 'testuser123',
    'password': 'StrongPass123!'
})
print("Login response status:", login_response.status_code)
if login_response.status_code == 302:
    print("Redirect to:", login_response.url)
else:
    print("Login failed form errors:")
    if login_response.context and login_response.context.get('form'):
        print(login_response.context.get('form').errors)
    else:
        print("No context or form available")

