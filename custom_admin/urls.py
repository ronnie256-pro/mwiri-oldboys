from django.urls import path
from .views import custom_admin_view

urlpatterns = [
    path("diabulogato", custom_admin_view, name="custom_admin"),
]
