
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import News
from .forms import NewsForm

def news_list(request):
    news = News.objects.all().order_by('-created_at')
    return render(request, 'content/news_list.html', {'news': news})

def news_form(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            return redirect('news_list')
    else:
        form = NewsForm()
    return render(request, 'content/news_form.html', {'form': form})

class NewsView(TemplateView):
    template_name = "content/news.html"
