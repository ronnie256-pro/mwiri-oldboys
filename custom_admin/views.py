import pyotp
from functools import wraps
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib.auth import get_user_model

from users.models import Profile
from products.models import Product, Service
from content.models import News, History, Category
from elections.models import Candidate, Position, ElectionCategory
from payments.models import Payment
from core.models import HeroSlider, SiteSettings

User = get_user_model()

# Custom Decorator ensuring User is Staff/Superuser AND 2FA Authenticated in session
def admin_dashboard_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, "Access restricted to authorized staff members.")
            return redirect('home')
        if not request.session.get('admin_2fa_verified', False):
            messages.error(request, "2FA authentication code required to access Admin Dashboard.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# 2FA Admin Login View
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        code = request.POST.get('code', '').strip()

        user = authenticate(request, username=username, password=password)
        if user is not None and (user.is_staff or user.is_superuser):
            # Fetch per-user TOTP secret key if set, or fallback to system setting
            profile, _ = Profile.objects.get_or_create(user=user)
            secret_key = profile.totp_secret or getattr(settings, 'ADMIN_2FA_SECRET_KEY', 'R4R2DVFXBJOCK74JVSK5EBQPIU2MWTYX')
            totp = pyotp.TOTP(secret_key)
            
            if totp.verify(code):
                login(request, user)
                request.session['admin_2fa_verified'] = True
                messages.success(request, f"Welcome to Admin Dashboard, {user.get_full_name() or user.username}!")
                return redirect('admin_dashboard_home')
            else:
                messages.error(request, "Invalid 2FA Google Authenticator code. Please check your app.")
        else:
            messages.error(request, "Invalid admin credentials or insufficient permissions.")
    return redirect('home')

def admin_logout(request):
    if 'admin_2fa_verified' in request.session:
        del request.session['admin_2fa_verified']
    logout(request)
    messages.success(request, "Logged out of Admin Dashboard.")
    return redirect('home')

# Dashboard Home Overview
@admin_dashboard_required
def dashboard_home(request):
    context = {
        'total_members': User.objects.count(),
        'verified_members': Profile.objects.filter(is_verified=True).count(),
        'total_products': Product.objects.count(),
        'pending_candidates': Candidate.objects.filter(status='PENDING').count(),
        'recent_members': User.objects.order_by('-date_joined')[:5],
        'recent_payments': Payment.objects.order_by('-created_at')[:5],
    }
    return render(request, 'admin/dashboard_home.html', context)

# Manage Members & Verification
@admin_dashboard_required
def manage_members(request):
    q = request.GET.get('q', '').strip()
    users = User.objects.select_related('profile', 'house', 'cohort', 'profession').all().order_by('-date_joined')
    if q:
        users = users.filter(username__icontains=q) | users.filter(first_name__icontains=q) | users.filter(last_name__icontains=q)
    return render(request, 'admin/manage_members.html', {'users': users, 'search_query': q})

@admin_dashboard_required
def toggle_user_verification(request, user_id):
    target_user = get_object_or_404(User, pk=user_id)
    profile, _ = Profile.objects.get_or_create(user=target_user)
    profile.is_verified = not profile.is_verified
    profile.save()
    status_str = "verified" if profile.is_verified else "unverified"
    messages.success(request, f"User '{target_user.username}' is now {status_str}.")
    return redirect('admin_members')

# Manage Products
@admin_dashboard_required
def manage_products(request):
    products = Product.objects.select_related('category', 'owner').all().order_by('-id')
    categories = Category.objects.all()
    return render(request, 'admin/manage_products.html', {'products': products, 'categories': categories})

# Manage Content (News & History)
@admin_dashboard_required
def manage_content(request):
    news_items = News.objects.select_related('category', 'author').all().order_by('-created_at')
    history_items = History.objects.select_related('category', 'author').all().order_by('-created_at')
    return render(request, 'admin/manage_content.html', {'news_items': news_items, 'history_items': history_items})

# Manage Elections & Candidate Status Toggle
@admin_dashboard_required
def manage_elections(request):
    candidates = Candidate.objects.select_related('user', 'position').all().order_by('-id')
    positions = Position.objects.all()
    return render(request, 'admin/manage_elections.html', {'candidates': candidates, 'positions': positions})

@admin_dashboard_required
def toggle_candidate_status(request, candidate_id, action):
    candidate = get_object_or_404(Candidate, pk=candidate_id)
    if action == 'approve':
        candidate.status = 'APPROVED'
        messages.success(request, f"Candidate {candidate.user.get_full_name() or candidate.user.username} has been APPROVED.")
    elif action == 'reject':
        candidate.status = 'DENIED'
        messages.warning(request, f"Candidate {candidate.user.get_full_name() or candidate.user.username} has been REJECTED.")
    candidate.save()
    return redirect('admin_elections')

# Manage Payments
@admin_dashboard_required
def manage_payments(request):
    payments = Payment.objects.select_related('user').all().order_by('-created_at')
    return render(request, 'admin/manage_payments.html', {'payments': payments})

# Manage Site Settings
@admin_dashboard_required
def manage_settings(request):
    hero_sliders = HeroSlider.objects.all()
    site_settings = SiteSettings.objects.first()
    return render(request, 'admin/manage_settings.html', {'hero_sliders': hero_sliders, 'site_settings': site_settings})