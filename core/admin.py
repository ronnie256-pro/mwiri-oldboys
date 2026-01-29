from django.contrib import admin
from .models import HeroSlider, Fixture, DidYouKnow

@admin.register(HeroSlider)
class HeroSliderAdmin(admin.ModelAdmin):
    list_display = ('hero_text',)

@admin.register(Fixture)
class FixtureAdmin(admin.ModelAdmin):
    list_display = ('cohort_1_name', 'cohort_2_name', 'date', 'location')

@admin.register(DidYouKnow)
class DidYouKnowAdmin(admin.ModelAdmin):
    list_display = ('date_of_event', 'description_of_event')
