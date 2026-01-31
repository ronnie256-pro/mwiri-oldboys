from django.contrib import admin
from .models import Product, ProductImage, Service

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'owner', 'price')
    list_filter = ('category',)
    search_fields = ('name', 'description', 'owner__username')

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'owner')
    list_filter = ('category',)
    search_fields = ('name', 'description', 'owner__username')
