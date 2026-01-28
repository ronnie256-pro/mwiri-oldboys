
from django.shortcuts import render
from content.models import News, Event
from products.models import Product

def home(request):
    latest_news = News.objects.order_by('-created_at')[:3]
    latest_events = Event.objects.order_by('-date')[:3]
    latest_products = Product.objects.order_by('-id')[:3]

    context = {
        'latest_news': latest_news,
        'latest_events': latest_events,
        'latest_products': latest_products,
    }
    return render(request, 'home.html', context)
