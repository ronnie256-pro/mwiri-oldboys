from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.admin.models import LogEntry
from django.contrib.auth import get_user_model

User = get_user_model()

@staff_member_required
def custom_admin_view(request):
    # Fetch log entries for the sidebar
    # We slice it here in Python to avoid the Template 'TypeError'
    admin_log = LogEntry.objects.select_related('content_type', 'user').order_by('-action_time')[:10]
    
    # Optional: Fetch some quick stats for the dashboard header
    total_users = User.objects.count()
    
    context = {
        'title': 'Admin Dashboard',
        'admin_log': admin_log,
        'total_users': total_users,
        # Adding 'user' explicitly to ensure it's available for template logic
        'user': request.user, 
    }
    
    return render(request, 'admin/admin.html', context)