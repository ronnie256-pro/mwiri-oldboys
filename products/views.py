from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.db.models import Q
from .models import Product, ProductImage, Service
from .forms import ProductForm, ServiceForm
from content.models import Category

class ProductListView(ListView):
    model = Product
    template_name = "products/products.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.select_related('category', 'owner').all()
        
        # Search query
        q = self.request.GET.get('q', '').strip()
        if q:
            queryset = queryset.filter(Q(name__icontains=q) | Q(description__icontains=q))

        # Category filter
        category_id = self.request.GET.get('category')
        if category_id and category_id.isdigit():
            queryset = queryset.filter(category_id=category_id)

        # Min Price filter
        min_price = self.request.GET.get('min_price')
        if min_price:
            try:
                queryset = queryset.filter(price__gte=float(min_price))
            except ValueError:
                pass

        # Max Price filter
        max_price = self.request.GET.get('max_price')
        if max_price:
            try:
                queryset = queryset.filter(price__lte=float(max_price))
            except ValueError:
                pass

        # Rating filter
        rating = self.request.GET.get('rating')
        if rating:
            try:
                queryset = queryset.filter(rating__gte=int(rating))
            except ValueError:
                pass

        # Sorting
        sort = self.request.GET.get('sort', 'newest')
        if sort == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort == 'price_desc':
            queryset = queryset.order_by('-price')
        elif sort == 'rating':
            queryset = queryset.order_by('-rating')
        else:  # newest
            queryset = queryset.order_by('-id')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['search_query'] = self.request.GET.get('q', '')
        context['selected_category'] = self.request.GET.get('category', '')
        context['min_price'] = self.request.GET.get('min_price', '')
        context['max_price'] = self.request.GET.get('max_price', '')
        context['selected_rating'] = self.request.GET.get('rating', '')
        context['selected_sort'] = self.request.GET.get('sort', 'newest')
        context['total_count'] = self.get_queryset().count()
        return context


class ServiceListView(ListView):
    model = Service
    template_name = "products/services.html"
    context_object_name = "services"

def product_form(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()

            for image in request.FILES.getlist('other_images'):
                ProductImage.objects.create(product=product, image=image)

            return redirect('products')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form})

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    # provide other products in the same category for 'More Items in Our Owino' section (up to 4)
    other_products = list(Product.objects.filter(category=product.category).exclude(pk=product.pk).order_by('?')[:4])

    # Ensure context has missing_count for blank fallback cards
    missing_count = max(0, 4 - len(other_products))

    return render(request, 'products/product_detail.html', {
        'product': product,
        'other_products': other_products,
        'missing_range': range(missing_count)
    })

def service_form(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.owner = request.user
            service.save()
            return redirect('services')
    else:
        form = ServiceForm()
    return render(request, 'products/service_form.html', {'form': form})
