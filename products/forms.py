from django import forms
from .models import Product, Service

class ProductForm(forms.ModelForm):
    other_images = forms.FileField(label='Other Images', required=False)

    class Meta:
        model = Product
        fields = ['name', 'description', 'hero_image', 'price', 'category']

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'category']
