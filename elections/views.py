from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Candidate
from .forms import CandidateApplicationForm

@login_required
def elections_home(request):
    return render(request, 'elections/elections_home.html')

@login_required
def apply_for_office(request):
    if Candidate.objects.filter(user=request.user).exists():
        messages.error(request, "You have already submitted a nomination. You can only run for one office.")
        return redirect('my_account')

    if request.method == 'POST':
        form = CandidateApplicationForm(request.POST)
        if form.is_valid():
            candidate = form.save(commit=False)
            candidate.user = request.user
            candidate.status = Candidate.STATUS_PENDING
            candidate.save()
            messages.success(request, "Your nomination has been submitted successfully and is pending approval.")
            return redirect('my_account')
    else:
        form = CandidateApplicationForm()

    return render(request, 'elections/apply_for_office.html', {'form': form})
