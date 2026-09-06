
from django.db import models
from django.conf import settings

class Category(models.Model):
    CATEGORY_MARKETPLACE = 'MARKETPLACE'
    CATEGORY_NEWS = 'NEWS'
    CATEGORY_HISTORY = 'HISTORY'

    CATEGORY_TYPE_CHOICES = [
        (CATEGORY_MARKETPLACE, 'Marketplace'),
        (CATEGORY_NEWS, 'News'),
        (CATEGORY_HISTORY, 'History'),
    ]

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    category_type = models.CharField(
        max_length=20,
        choices=CATEGORY_TYPE_CHOICES,
        default=CATEGORY_NEWS
    )

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name} ({self.get_category_type_display()})"

class News(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    hero_image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='news')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            base_slug = slugify(self.title) or "news"
            slug = base_slug
            counter = 1
            while News.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        if self.hero_image:
            from core.image_utils import convert_to_webp
            convert_to_webp(self.hero_image)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class NewsImage(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='extra_images')
    image = models.ImageField(upload_to='news_images/')

    def save(self, *args, **kwargs):
        if self.image:
            from core.image_utils import convert_to_webp
            convert_to_webp(self.image)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.news.title

class Event(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='content_products')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Gallery(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='gallery_images')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.image:
            from core.image_utils import convert_to_webp
            convert_to_webp(self.image)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class History(models.Model):
    title = models.CharField(max_length=200)
    hero_image = models.ImageField(upload_to='history_images/', blank=True, null=True)
    pdf_file = models.FileField(upload_to='history_pdfs/', blank=True, null=True)
    content = models.TextField(blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='history_entries')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.hero_image:
            from core.image_utils import convert_to_webp
            convert_to_webp(self.hero_image)
        super().save(*args, **kwargs)

    @property
    def filename(self):
        if self.pdf_file:
            import os
            return os.path.basename(self.pdf_file.name)
        return ""

    def __str__(self):
        return self.title

class HistoryImage(models.Model):
    history = models.ForeignKey(History, on_delete=models.CASCADE, related_name='extra_images')
    image = models.ImageField(upload_to='history_images/')

    def save(self, *args, **kwargs):
        if self.image:
            from core.image_utils import convert_to_webp
            convert_to_webp(self.image)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.history.title
