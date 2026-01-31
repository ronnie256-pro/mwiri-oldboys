
from django.shortcuts import render
from content.models import News, Event
from products.models import Product
from .models import HeroSlider, Fixture, ManOfTheHour

def home(request):
    latest_news = News.objects.order_by('-created_at')[:3]
    latest_events = Event.objects.order_by('-date')[:3]
    latest_products = Product.objects.order_by('-id')[:3]
    hero_slides = HeroSlider.objects.all()
    fixtures = Fixture.objects.order_by('date')[:1]
    man_of_the_hour = ManOfTheHour.objects.order_by('?')[:1]

    context = {
        'latest_news': latest_news,
        'latest_events': latest_events,
        'latest_products': latest_products,
        'hero_slides': hero_slides,
        'fixtures': fixtures,
        'man_of_the_hour': man_of_the_hour,
    }
    return render(request, 'home.html', context)
