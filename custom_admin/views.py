import pyotp
from functools import wraps
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.text import slugify

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

from django.db.models import Q
from organisation.models import House, Cohort

# Manage Members & Verification
@admin_dashboard_required
def manage_members(request):
    q = request.GET.get('q', '').strip()
    house_id = request.GET.get('house', '').strip()
    cohort_id = request.GET.get('cohort', '').strip()
    verification = request.GET.get('verification', '').strip()

    users = User.objects.select_related('profile', 'house', 'cohort', 'profession').all().order_by('-date_joined')

    if q:
        users = users.filter(
            Q(username__icontains=q) | 
            Q(first_name__icontains=q) | 
            Q(last_name__icontains=q) | 
            Q(email__icontains=q)
        )

    if house_id:
        users = users.filter(house_id=house_id)

    if cohort_id:
        users = users.filter(cohort_id=cohort_id)

    if verification == 'verified':
        users = users.filter(profile__is_verified=True)
    elif verification == 'unverified':
        users = users.filter(Q(profile__is_verified=False) | Q(profile__isnull=True))

    houses = House.objects.all().order_by('name')
    cohorts = Cohort.objects.all().order_by('name')

    context = {
        'users': users,
        'search_query': q,
        'selected_house': house_id,
        'selected_cohort': cohort_id,
        'selected_verification': verification,
        'houses': houses,
        'cohorts': cohorts,
    }
    return render(request, 'admin/manage_members.html', context)

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
    categories = Category.objects.filter(category_type=Category.CATEGORY_MARKETPLACE).order_by('name')
    return render(request, 'admin/manage_products.html', {'products': products, 'categories': categories})

@admin_dashboard_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product_name = product.name
    product.delete()
    messages.success(request, f"Product '{product_name}' has been successfully deleted.")
    return redirect('admin_products')

# Manage Content (News & History)
@admin_dashboard_required
def manage_content(request):
    news_items = News.objects.select_related('category', 'author').all().order_by('-created_at')
    history_items = History.objects.select_related('category', 'author').all().order_by('-created_at')
    news_categories = Category.objects.filter(category_type=Category.CATEGORY_NEWS).order_by('name')
    history_categories = Category.objects.filter(category_type=Category.CATEGORY_HISTORY).order_by('name')
    return render(request, 'admin/manage_content.html', {
        'news_items': news_items,
        'history_items': history_items,
        'news_categories': news_categories,
        'history_categories': history_categories,
    })

@admin_dashboard_required
def delete_news(request, news_id):
    news_item = get_object_or_404(News, pk=news_id)
    title = news_item.title
    news_item.delete()
    messages.success(request, f"News article '{title}' has been successfully deleted.")
    return redirect('admin_content')

@admin_dashboard_required
def delete_history(request, history_id):
    history_item = get_object_or_404(History, pk=history_id)
    title = history_item.title
    history_item.delete()
    messages.success(request, f"History archive '{title}' has been successfully deleted.")
    return redirect('admin_content')

# Dynamic Domain Category Creation & Deletion
@admin_dashboard_required
def add_admin_category(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        category_type = request.POST.get('category_type', '').strip()
        redirect_to = request.POST.get('redirect_to', 'admin_products')
        
        valid_types = [Category.CATEGORY_MARKETPLACE, Category.CATEGORY_NEWS, Category.CATEGORY_HISTORY]
        if not name or category_type not in valid_types:
            messages.error(request, "Invalid category name or category domain type.")
            return redirect(redirect_to)

        slug = slugify(name)
        if not slug:
            messages.error(request, "Please enter a valid category name.")
            return redirect(redirect_to)

        if Category.objects.filter(slug=slug).exists():
            messages.error(request, f"Category with name '{name}' already exists.")
            return redirect(redirect_to)

        Category.objects.create(
            name=name,
            slug=slug,
            category_type=category_type
        )
        messages.success(request, f"Category '{name}' created successfully.")
        return redirect(redirect_to)
    return redirect('admin_dashboard_home')

@admin_dashboard_required
def delete_admin_category(request, category_id):
    if request.method == 'POST':
        category = get_object_or_404(Category, pk=category_id)
        redirect_to = request.POST.get('redirect_to', 'admin_products')
        cat_name = category.name
        category.delete()
        messages.success(request, f"Category '{cat_name}' deleted successfully.")
        return redirect(redirect_to)
    return redirect('admin_dashboard_home')


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