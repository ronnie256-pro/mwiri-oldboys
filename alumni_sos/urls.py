from django.urls import path
from .views import alumni_sos_view

urlpatterns = [
    path("alumni-sos/", alumni_sos_view, name="alumni_sos"),
]
