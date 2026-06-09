from django.contrib import admin
from .models import HeroSlider, Fixture, ManOfTheHour, SiteSettings

@admin.register(HeroSlider)
class HeroSliderAdmin(admin.ModelAdmin):
    list_display = ('hero_text',)

@admin.register(Fixture)
class FixtureAdmin(admin.ModelAdmin):
    list_display = ('cohort_1_name', 'cohort_2_name', 'date', 'location')

@admin.register(ManOfTheHour)
class ManOfTheHourAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'site_logo', 'site_icon')
    
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)
