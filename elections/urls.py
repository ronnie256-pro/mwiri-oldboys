from django.urls import path
from . import views

urlpatterns = [
    path('', views.elections_home, name='elections'),
    path('apply/', views.apply_for_office, name='apply_for_office'),
]
