
from django.contrib import admin
from .models import Category, News, NewsImage, History, HistoryImage
from products.models import Product

class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 1

class HistoryImageInline(admin.TabularInline):
    model = HistoryImage
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'is_featured', 'created_at')
    list_filter = ('is_featured', 'category', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [NewsImageInline]

@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    list_filter = ('category',)
    search_fields = ('title', 'content')
    inlines = [HistoryImageInline]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')
    list_filter = ('category',)
    search_fields = ('name', 'description')
