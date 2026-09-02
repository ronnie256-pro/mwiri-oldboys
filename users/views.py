from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib import messages
from .forms import RegistrationForm, ProfileForm, SideHustleForm
from alumni_sos.forms import SOSRequestForm
from teaser.forms import TeaserQuestionForm
from .models import User, Profile, SideHustle
from teaser.models import TeaserQuestion

from django.http import JsonResponse
from django.urls import reverse

def register(request):
    teaser_questions = TeaserQuestion.objects.all()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        teaser_form = TeaserQuestionForm(request.POST, questions=teaser_questions)

        if form.is_valid() and teaser_form.is_valid():
            all_correct = True
            for question in teaser_questions:
                selected_answer = teaser_form.cleaned_data.get(f'question_{question.id}')
                correct_answer = question.answers.filter(is_correct=True).first()
                
                # If no answer was selected, or the question doesn't have a correct answer set in the admin, or they don't match
                if not selected_answer or not correct_answer or selected_answer.id != correct_answer.id:
                    all_correct = False
                    break
            
            if all_correct:
                if 'teaser_attempts' in request.session:
                    del request.session['teaser_attempts']
                user = form.save(commit=False)
                user.is_active = True
                user.save()
                Profile.objects.create(user=user)
                messages.success(request, 'Your account has been created successfully, please login')
                
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': True, 'redirect_url': reverse('login')})
                return redirect('login')
            else:
                attempts = request.session.get('teaser_attempts', 0)
                attempts += 1
                request.session['teaser_attempts'] = attempts
                
                if attempts >= 2:
                    del request.session['teaser_attempts']
                    messages.error(request, 'Gundi, you are not a Mwirian')
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                        return JsonResponse({'success': False, 'error': 'Gundi, you are not a Mwirian', 'reset': True})
                    return redirect('register')
                else:
                    messages.error(request, 'Incorrect answers. You have one attempt remaining.')
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                        return JsonResponse({'success': False, 'error': 'Incorrect answers. You have one attempt remaining.', 'reset': False})
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
            side_hustle_form = SideHustleForm()
            side_hustles = request.user.side_hustles.all()
        else:
            form = None
            sos_form = None
            side_hustle_form = None
            side_hustles = None
        
        content_types = ["Products", "Services", "News", "History"]
        return render(request, self.template_name, {
            'form': form, 
            'sos_form': sos_form, 
            'content_types': content_types, 
            'side_hustle_form': side_hustle_form,
            'side_hustles': side_hustles
        })

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

        if 'update_years' in request.POST:
            profile, _ = Profile.objects.get_or_create(user=request.user)
            years_from = request.POST.get('years_from')
            years_to = request.POST.get('years_to')
            s4_year = request.POST.get('s4_year')
            s6_year = request.POST.get('s6_year')
            nickname = request.POST.get('nickname')
            
            if years_from:
                profile.years_at_mwiri_from = int(years_from)
            else:
                profile.years_at_mwiri_from = None
                
            if years_to:
                profile.years_at_mwiri_to = int(years_to)
            else:
                profile.years_at_mwiri_to = None

            if s4_year:
                profile.s4_year = int(s4_year)
            else:
                profile.s4_year = None
                
            if s6_year:
                profile.s6_year = int(s6_year)
            else:
                profile.s6_year = None
                
            if nickname is not None:
                profile.nickname = nickname.strip()
                
            profile.save()
            messages.success(request, 'School details updated successfully!')
            return redirect('my_account')

        if 'submit_sos' in request.POST:
            return redirect('alumni_sos')

        if 'add_side_hustle' in request.POST:
            if request.user.side_hustles.count() >= 2:
                messages.error(request, 'You can only have a maximum of 2 side hustles.')
                return redirect('my_account')
            
            side_hustle_form = SideHustleForm(request.POST, request.FILES)
            if side_hustle_form.is_valid():
                hustle = side_hustle_form.save(commit=False)
                hustle.user = request.user
                hustle.save()
                messages.success(request, 'Side hustle added successfully!')
                return redirect('my_account')
            else:
                messages.error(request, 'Error adding side hustle. Please check the form.')

        content_types = ["Products", "Services", "News", "History"]
        side_hustle_form = SideHustleForm()
        side_hustles = request.user.side_hustles.all()
        return render(request, self.template_name, {
            'form': form, 
            'sos_form': sos_form, 
            'content_types': content_types, 
            'side_hustle_form': side_hustle_form,
            'side_hustles': side_hustles
        })

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        return redirect('my_account')

def logout_view(request):
    logout(request)
    return redirect('home')

