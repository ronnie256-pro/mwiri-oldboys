from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import SOSRequest
from .forms import SOSRequestForm

@login_required
def alumni_sos_view(request):
    sos_requests = SOSRequest.objects.all().order_by('-created_at')
    return render(request, 'alumni_sos/alumni_sos.html', {'sos_requests': sos_requests})
