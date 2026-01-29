from django.contrib import admin
from .models import Cohort, House, Profession, Committee

@admin.register(Cohort)
class CohortAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Profession)
class ProfessionAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Committee)
class CommitteeAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'cohort')
    list_filter = ('cohort',)
    search_fields = ('name', 'position')
