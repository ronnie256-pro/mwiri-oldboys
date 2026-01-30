from django.shortcuts import render
from django.views.generic import TemplateView
from organisation.models import Committee
from .models import LegacyPhoto

# Create your views here.

class AboutPageView(TemplateView):
    template_name = "pages/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['committee_members'] = Committee.objects.all()
        context['legacy_photo'] = LegacyPhoto.objects.first()
        return context

class HistoryView(TemplateView):
    template_name = "pages/history.html"
