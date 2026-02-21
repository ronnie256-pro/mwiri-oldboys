from django.contrib import admin
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from .models import FeaturedNews

# Try to discover the project's News model from common app labels
NewsModel = None
for app_label in ('content', 'news', 'articles', 'posts', 'blog'):
    try:
        NewsModel = apps.get_model(app_label, 'News')
        if NewsModel:
            break
    except LookupError:
        continue


class FeaturedNewsForm(forms.ModelForm):
    if NewsModel:
        news_article = forms.ModelChoiceField(queryset=NewsModel.objects.all(), required=False, label='News Article')

    class Meta:
        model = FeaturedNews
        fields = ('slot', 'title', 'hero_image', 'order', 'active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # insert the news_article field at the top if available
        if NewsModel:
            if self.instance and self.instance.pk and self.instance.content_type and self.instance.object_id:
                try:
                    model_class = self.instance.content_type.model_class()
                    if model_class and model_class == NewsModel:
                        self.fields['news_article'].initial = NewsModel.objects.filter(pk=self.instance.object_id).first()
                except Exception:
                    pass

    def save(self, commit=True):
        instance = super().save(commit=False)
        # if admin selected a News article, set the generic relation fields
        if NewsModel and 'news_article' in self.cleaned_data and self.cleaned_data.get('news_article'):
            article = self.cleaned_data['news_article']
            instance.content_type = ContentType.objects.get_for_model(article)
            instance.object_id = article.pk
        if commit:
            instance.save()
        return instance


@admin.register(FeaturedNews)
class FeaturedNewsAdmin(admin.ModelAdmin):
    form = FeaturedNewsForm
    list_display = ('slot', 'get_title', 'linked_article', 'order', 'active')
    list_filter = ('slot', 'active')
    search_fields = ('title',)
    ordering = ('slot', 'order')

    def linked_article(self, obj):
        try:
            return getattr(obj.article, 'title', None) or obj.get_title()
        except Exception:
            return obj.get_title()
    linked_article.short_description = 'Article'
