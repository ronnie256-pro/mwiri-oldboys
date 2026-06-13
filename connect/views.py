
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Value
from django.db.models.functions import Concat
from users.models import User
from organisation.models import Cohort, Profession, House

@login_required
def ob_connect(request):
    users = User.objects.all().order_by('-date_joined')
    cohorts = Cohort.objects.all().order_by('name')
    professions = Profession.objects.all().order_by('name')
    houses = House.objects.all().order_by('name')

    name_query = request.GET.get('name')
    cohort_query = request.GET.get('cohort')
    profession_query = request.GET.get('profession')
    house_query = request.GET.get('house')
    year_from_query = request.GET.get('year_from')
    year_to_query = request.GET.get('year_to')
    s4_year_query = request.GET.get('s4_year')
    s6_year_query = request.GET.get('s6_year')

    if name_query:
        name_query = name_query.strip()
        users = users.annotate(
            search_name=Concat('first_name', Value(' '), 'last_name')
        ).filter(
            Q(first_name__icontains=name_query) | 
            Q(last_name__icontains=name_query) | 
            Q(username__icontains=name_query) |
            Q(search_name__icontains=name_query)
        )
        
    if cohort_query:
        users = users.filter(cohort_id=cohort_query)
    if profession_query:
        users = users.filter(profession_id=profession_query)
    if house_query:
        users = users.filter(house_id=house_query)
        
    if year_from_query and year_from_query.isdigit():
        users = users.filter(profile__years_at_mwiri_from__gte=int(year_from_query))
        
    if year_to_query and year_to_query.isdigit():
        users = users.filter(profile__years_at_mwiri_to__lte=int(year_to_query))
        
    if s4_year_query and s4_year_query.isdigit():
        users = users.filter(profile__s4_year=int(s4_year_query))
        
    if s6_year_query and s6_year_query.isdigit():
        users = users.filter(profile__s6_year=int(s6_year_query))

    # Pagination logic
    page = request.GET.get('page', 1)
    paginator = Paginator(users, 20) # 20 users per page
    try:
        paginated_users = paginator.page(page)
    except PageNotAnInteger:
        paginated_users = paginator.page(1)
    except EmptyPage:
        paginated_users = paginator.page(paginator.num_pages)

    context = {
        'users': paginated_users,
        'cohorts': cohorts,
        'professions': professions,
        'houses': houses,
    }
    return render(request, 'connect/ob_connect.html', context)

@login_required
def view_ob(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, 'connect/view_ob.html', {'user': user})
