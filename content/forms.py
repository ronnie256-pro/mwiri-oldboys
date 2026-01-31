from django import forms
from .models import News, History

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'hero_image', 'category']

class HistoryForm(forms.ModelForm):
    class Meta:
        model = History
        fields = ['title', 'content', 'hero_image', 'category']
