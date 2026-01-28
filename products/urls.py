from django.urls import path
from .views import ProductListView, ServiceListView

urlpatterns = [
    path("products/", ProductListView.as_view(), name="products"),
    path("services/", ServiceListView.as_view(), name="services"),
]
