
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import User

@login_required
def ob_connect(request):
    users = User.objects.filter(role=User.Role.SUBSCRIBER)
    return render(request, 'connect/ob_connect.html', {'users': users})
