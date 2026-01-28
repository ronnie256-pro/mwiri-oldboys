from django.urls import path
from .views import ProductListView, ServiceListView, product_form

urlpatterns = [
    path("products/", ProductListView.as_view(), name="products"),
    path("products/add/", product_form, name="product_add"),
    path("services/", ServiceListView.as_view(), name="services"),
    path("services/add/", product_form, name="service_add"),
]
