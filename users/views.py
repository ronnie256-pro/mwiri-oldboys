from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib import messages
from .forms import RegistrationForm, ProfileForm
from .models import User, Profile

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True  # Activate user immediately
            user.save()
            messages.success(request, 'Your account has been created successfully!')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})

from django.views import View

class MyAccountView(View):
    template_name = 'users/my_account.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = ProfileForm(instance=request.user)
        else:
            form = None
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        if 'upload_picture' in request.POST:
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
        else:
            form = ProfileForm(instance=request.user)

        return render(request, self.template_name, {'form': form})

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        if self.request.user.role == User.Role.ADMIN:
            return redirect('admin_redirect')
        else:
            return redirect('my_account')

@login_required
def admin_redirect_view(request):
    return redirect('custom_admin')

class AdminView(TemplateView):
    template_name = 'users/admin.html'
