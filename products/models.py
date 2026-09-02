from django.db import models
from django.contrib.auth import get_user_model
from content.models import Category

User = get_user_model()

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    hero_image = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    quantity = models.PositiveIntegerField(default=1)
    rating = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.hero_image:
            from core.image_utils import convert_to_webp
            convert_to_webp(self.hero_image)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')

    def save(self, *args, **kwargs):
        if self.image:
            from core.image_utils import convert_to_webp
            convert_to_webp(self.image)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product.name

class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='services')

    def __str__(self):
        return self.name
