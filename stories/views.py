from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from .models import Story
from .forms import StoryForm


@login_required
def add_story(request):
    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.author = request.user
            story.save()
            return redirect('our_stories')
    else:
        form = StoryForm()
    return render(request, 'stories/add_story_form.html', {'form': form})


class OurStoriesView(ListView):
    model = Story
    template_name = 'stories/our_stories.html'
    context_object_name = 'stories'

    def get_queryset(self):
        return Story.objects.filter(is_approved=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['story_form'] = StoryForm()
        return context


class StoryDetailView(DetailView):
    model = Story
    template_name = 'stories/story_detail.html'
    context_object_name = 'story'