from django.contrib import admin
from .models import LegacyPhoto

@admin.register(LegacyPhoto)
class LegacyPhotoAdmin(admin.ModelAdmin):
    list_display = ('caption',)
