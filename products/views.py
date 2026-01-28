from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import Product
from .forms import ProductForm

class ProductListView(ListView):
    model = Product
    template_name = "products/products.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.filter(product_type='PR')

class ServiceListView(ListView):
    model = Product
    template_name = "products/services.html"
    context_object_name = "services"

    def get_queryset(self):
        return Product.objects.filter(product_type='SR')

def product_form(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            if product.product_type == 'PR':
                return redirect('products')
            else:
                return redirect('services')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form})
