from django.views.generic import ListView, TemplateView
from .models import Product

class ProductListView(ListView):
    model = Product
    template_name = "products/products.html"
    context_object_name = "products"

class ServiceListView(TemplateView):
    template_name = "products/services.html"
