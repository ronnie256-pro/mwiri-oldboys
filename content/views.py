
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import News
from .forms import NewsForm

def news_list(request):
    news = News.objects.all().order_by('-created_at')
    return render(request, 'content/news_list.html', {'news': news})

from .models import News, NewsImage, History, HistoryImage
from .forms import NewsForm, HistoryForm

def news_form(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            for image in request.FILES.getlist('extra_images'):
                NewsImage.objects.create(news=news, image=image)
            return redirect('news_list')
    else:
        form = NewsForm()
    return render(request, 'content/news_form.html', {'form': form, 'extra_images': True})

def history_form(request):
    if request.method == 'POST':
        form = HistoryForm(request.POST, request.FILES)
        if form.is_valid():
            history = form.save(commit=False)
            history.author = request.user
            history.save()
            for image in request.FILES.getlist('extra_images'):
                HistoryImage.objects.create(history=history, image=image)
            return redirect('history_list')
    else:
        form = HistoryForm()
    return render(request, 'content/history_form.html', {'form': form, 'extra_images': True})

def history_list(request):
    history = History.objects.all().order_by('-created_at')
    return render(request, 'content/history_list.html', {'history': history})

class NewsView(TemplateView):
    template_name = "content/news.html"
