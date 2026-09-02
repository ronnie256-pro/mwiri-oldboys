from django.urls import path
from .views import AboutPageView
from content.views import history_list

urlpatterns = [
    path("about/", AboutPageView.as_view(), name="about"),
    path("history/", history_list, name="history"),
]
