from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import Product, ProductImage, Service
from .forms import ProductForm, ServiceForm

class ProductListView(ListView):
    model = Product
    template_name = "products/products.html"
    context_object_name = "products"


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
    product = Product.objects.get(id=product_id)
    return render(request, 'products/product_detail.html', {'product': product})

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
