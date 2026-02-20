from django.urls import path
from .views import OurStoriesView, StoryDetailView, add_story

urlpatterns = [
    path('stories/', OurStoriesView.as_view(), name='our_stories'),
    path('stories/add/', add_story, name='add_story'),
    path('stories/<int:pk>/', StoryDetailView.as_view(), name='story_detail'),
]