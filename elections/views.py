from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Candidate, ElectionCategory
from .forms import CandidateApplicationForm

@login_required
def elections_home(request):
    categories = ElectionCategory.objects.filter(is_active=True).prefetch_related(
        'positions',
        'positions__candidates',
        'positions__candidates__user'
    )
    return render(request, 'elections/elections_home.html', {'categories': categories})

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

@login_required
def candidate_manifesto(request, id):
    candidate = get_object_or_404(Candidate, id=id)
    return render(request, 'elections/manifesto.html', {'candidate': candidate})
