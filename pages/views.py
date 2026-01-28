from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class AboutPageView(TemplateView):
    template_name = "pages/about.html"

class HistoryView(TemplateView):
    template_name = "pages/history.html"
