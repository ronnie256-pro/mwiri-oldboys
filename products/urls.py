from django.urls import path
from .views import ProductListView, ServiceListView, product_form, product_detail, service_form

urlpatterns = [
    path("products/", ProductListView.as_view(), name="products"),
    path("products/add/", product_form, name="product_add"),
    path("products/<int:product_id>/", product_detail, name="product_detail"),
    path("services/", ServiceListView.as_view(), name="services"),
    path("services/add/", service_form, name="service_add"),
]
