from django import forms
from .models import News, History, Category

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'hero_image', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(category_type=Category.CATEGORY_NEWS)

class HistoryForm(forms.ModelForm):
    class Meta:
        model = History
        fields = ['title', 'content', 'hero_image', 'pdf_file', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(category_type=Category.CATEGORY_HISTORY)

