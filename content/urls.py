
from django.urls import path
from . import views

urlpatterns = [
    path('news/', views.news_list, name='news'),
    path('news/add/', views.news_form, name='news_add'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    path('history/', views.history_list, name='history'),
    path('history/add/', views.history_form, name='history_add'),
    path('history/<int:pk>/', views.history_detail, name='history_detail'),
]
