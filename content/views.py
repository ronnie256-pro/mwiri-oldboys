
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import News

def news_list(request):
    news = News.objects.all().order_by('-created_at')
    return render(request, 'content/news_list.html', {'news': news})

class NewsView(TemplateView):
    template_name = "content/news.html"
