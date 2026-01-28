from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    class ProductType(models.TextChoices):
        PRODUCT = 'PR', 'Product'
        SERVICE = 'SR', 'Service'

    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    contact = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_type = models.CharField(
        max_length=2,
        choices=ProductType.choices,
        default=ProductType.PRODUCT,
    )
    rating = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
