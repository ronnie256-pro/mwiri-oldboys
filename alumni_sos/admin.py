from django.contrib import admin
from .models import SOSRequest

@admin.register(SOSRequest)
class SOSRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'requester', 'created_at', 'deadline')
    list_filter = ('created_at', 'deadline')
    search_fields = ('title', 'description', 'requester__username')
