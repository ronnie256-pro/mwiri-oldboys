from django import forms
from .models import Story


class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['title', 'content', 'hero_image', 'additional_image_1', 'additional_image_2', 'additional_image_3']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 6}),
        }