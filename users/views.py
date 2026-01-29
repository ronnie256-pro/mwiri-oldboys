from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib import messages
from .forms import RegistrationForm, ProfileForm
from alumni_sos.forms import SOSRequestForm
from teaser.forms import TeaserQuestionForm
from .models import User, Profile
from teaser.models import TeaserQuestion

def register(request):
    teaser_questions = TeaserQuestion.objects.all()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        teaser_form = TeaserQuestionForm(request.POST, questions=teaser_questions)

        if form.is_valid() and teaser_form.is_valid():
            all_correct = True
            for question in teaser_questions:
                selected_answer_id = teaser_form.cleaned_data.get(f'question_{question.id}').id
                correct_answer = question.answers.get(is_correct=True)
                if selected_answer_id != correct_answer.id:
                    all_correct = False
                    break
            
            if all_correct:
                user = form.save(commit=False)
                user.is_active = True
                user.save()
                messages.success(request, 'Your account has been created successfully!')
                return redirect('login')
            else:
                messages.error(request, 'You are not a Mwirian')
    else:
        form = RegistrationForm()
        teaser_form = TeaserQuestionForm(questions=teaser_questions)
    return render(request, 'users/register.html', {'form': form, 'teaser_form': teaser_form})

from django.views import View

class MyAccountView(View):
    template_name = 'users/my_account.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = ProfileForm(instance=request.user)
            sos_form = SOSRequestForm()
        else:
            form = None
            sos_form = None
        
        content_types = ["Products", "Services", "News", "History"]
        return render(request, self.template_name, {'form': form, 'sos_form': sos_form, 'content_types': content_types})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        form = ProfileForm(instance=request.user)
        sos_form = SOSRequestForm()

        if 'profile_picture' in request.FILES:
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.profile_picture = request.FILES.get('profile_picture')
            profile.save()
            messages.success(request, 'Profile picture updated successfully!')
            return redirect('my_account')

        if 'update_profile' in request.POST:
            form = ProfileForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('my_account')

        if 'submit_sos' in request.POST:
            return redirect('alumni_sos')

        content_types = ["Products", "Services", "News", "History"]
        return render(request, self.template_name, {'form': form, 'sos_form': sos_form, 'content_types': content_types})

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        return redirect('my_account')

def logout_view(request):
    logout(request)
    return redirect('home')

