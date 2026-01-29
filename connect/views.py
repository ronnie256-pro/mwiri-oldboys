
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import User
from organisation.models import Cohort, Profession, House

@login_required
def ob_connect(request):
    users = User.objects.all()
    cohorts = Cohort.objects.all()
    professions = Profession.objects.all()
    houses = House.objects.all()

    name_query = request.GET.get('name')
    cohort_query = request.GET.get('cohort')
    profession_query = request.GET.get('profession')
    house_query = request.GET.get('house')

    if name_query:
        users = users.filter(first_name__icontains=name_query) | users.filter(last_name__icontains=name_query)
    if cohort_query:
        users = users.filter(cohort_id=cohort_query)
    if profession_query:
        users = users.filter(profession_id=profession_query)
    if house_query:
        users = users.filter(house_id=house_query)

    context = {
        'users': users,
        'cohorts': cohorts,
        'professions': professions,
        'houses': houses,
    }
    return render(request, 'connect/ob_connect.html', context)

@login_required
def view_ob(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, 'connect/view_ob.html', {'user': user})
