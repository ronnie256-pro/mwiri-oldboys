from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import Product, ProductImage
from .forms import ProductForm

class ProductListView(ListView):
    model = Product
    template_name = "products/products.html"
    context_object_name = "products"

class ServiceListView(ListView):
    model = Product
    template_name = "products/services.html"
    context_object_name = "services"

def product_form(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()

            for image in request.FILES.getlist('images'):
                ProductImage.objects.create(product=product, image=image)

            return redirect('products')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form})

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'products/product_detail.html', {'product': product})
