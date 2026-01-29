from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import SOSRequest
from .forms import SOSRequestForm

@login_required
def alumni_sos_view(request):
    if request.method == 'POST':
        form = SOSRequestForm(request.POST)
        if form.is_valid():
            sos_request = form.save(commit=False)
            sos_request.requester = request.user
            sos_request.save()
            return redirect('alumni_sos')
    else:
        form = SOSRequestForm()
    
    sos_requests = SOSRequest.objects.all().order_by('-created_at')
    return render(request, 'alumni_sos/alumni_sos.html', {'sos_requests': sos_requests, 'form': form})
