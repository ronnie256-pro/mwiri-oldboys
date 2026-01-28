from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.admin.models import LogEntry

@staff_member_required
def custom_admin_view(request):
    context = {
        'title': 'Admin Dashboard',
        'log_entries': LogEntry.objects.select_related('content_type', 'user').order_by('-action_time')[:10]
    }
    return render(request, 'admin/admin.html', context)
