from django.contrib import admin
from .models import Cohort, House

@admin.register(Cohort)
class CohortAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ('name',)
