from django.urls import path
from .views import AboutPageView, HistoryView

urlpatterns = [
    path("about/", AboutPageView.as_view(), name="about"),
    path("history/", HistoryView.as_view(), name="history"),
]
