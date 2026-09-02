
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import Category, News, NewsImage, History, HistoryImage
from .forms import NewsForm, HistoryForm

def news_list(request):
    q = request.GET.get('q', '').strip()
    queryset = News.objects.select_related('category', 'author').all().order_by('-created_at')
    if q:
        queryset = queryset.filter(title__icontains=q)
    return render(request, 'content/news_list.html', {'news': queryset, 'search_query': q})


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
    q = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '').strip()
    queryset = History.objects.select_related('category', 'author').filter(pdf_file__isnull=False).exclude(pdf_file='').order_by('-created_at')
    if q:
        queryset = queryset.filter(title__icontains=q)
    if category_id and category_id.isdigit():
        queryset = queryset.filter(category_id=category_id)

    categories = Category.objects.all()
    return render(request, 'content/history_list.html', {
        'history': queryset,
        'categories': categories,
        'search_query': q,
        'selected_category': category_id,
        'total_count': queryset.count(),
    })

from django.shortcuts import get_object_or_404

def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)
    # Split content into paragraphs for inline image insertion
    content_paragraphs = [p.strip() for p in news.content.split('\n') if p.strip()]

    # Up to 3 extra images and fallback missing count
    extra_images = list(news.extra_images.all()[:3])
    missing_count = max(0, 3 - len(extra_images))

    return render(request, 'content/news_detail.html', {
        'news': news,
        'content_paragraphs': content_paragraphs,
        'extra_images': extra_images,
        'missing_range': range(missing_count),
    })

def history_detail(request, pk):
    history = get_object_or_404(History, pk=pk)
    return render(request, 'content/history_detail.html', {'history': history})
