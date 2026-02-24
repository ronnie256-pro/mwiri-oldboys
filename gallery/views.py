from django.shortcuts import render, get_object_or_404
from .models import GalleryCategory, Image


def gallery_view(request):
    categories = GalleryCategory.objects.all()
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(GalleryCategory, slug=category_slug)
        images = Image.objects.filter(category=category).order_by('-uploaded_at')
    else:
        category = None
        images = Image.objects.all().order_by('-uploaded_at')

    return render(request, 'gallery/gallery.html', {'categories': categories, 'images': images, 'active_category': category})
