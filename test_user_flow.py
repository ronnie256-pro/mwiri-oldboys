import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moba.settings")
django.setup()

from django.test import Client
from teaser.models import TeaserQuestion

client = Client()

questions = TeaserQuestion.objects.all()
teaser_data = {}
for q in questions:
    correct_ans = q.answers.filter(is_correct=True).first()
    if correct_ans:
        teaser_data[f'question_{q.id}'] = correct_ans.id

data = {
    'username': 'Ronnie3',
    'password1': 'Ronnie123!',
    'password2': 'Ronnie123!',
    'first_name': 'Ronnie',
    'last_name': 'Test',
    'email': 'ronnie3@test.com',
    'phone_number': '1234567890',
}
data.update(teaser_data)

response = client.post('/accounts/register/', data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
print("Register response:", response.status_code)
if response.status_code == 200:
    if response.headers.get('Content-Type').startswith('application/json'):
        print("JSON:", response.json())
    else:
        print("HTML content:", response.content.decode()[:1000])

