
from django.urls import path
from . import views

urlpatterns = [
    path('ob-connect/', views.ob_connect, name='ob_connect'),
]
