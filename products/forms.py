from django import forms
from .models import Product, Service
from content.models import Category

class ProductForm(forms.ModelForm):
    other_images = forms.FileField(label='Other Images', required=False)

    class Meta:
        model = Product
        fields = ['name', 'description', 'hero_image', 'price', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(category_type=Category.CATEGORY_MARKETPLACE)

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(category_type=Category.CATEGORY_MARKETPLACE)

