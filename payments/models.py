from django.db import models
from django.conf import settings
from django.utils import timezone
from decimal import Decimal


class Payment(models.Model):
    STATUS_PENDING = 'PENDING'
    STATUS_SUCCESS = 'SUCCESS'
    STATUS_FAILED = 'FAILED'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_SUCCESS, 'Success'),
        (STATUS_FAILED, 'Failed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    tx_ref = models.CharField(max_length=255, unique=True)
    flw_ref = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    currency = models.CharField(max_length=10, default='UGX')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    email = models.EmailField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=32, blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.tx_ref} ({self.status})"


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user}"

    def total_amount(self):
        total = Decimal('0.00')
        for item in self.items.all():
            total += (item.price or Decimal('0.00')) * item.quantity
        return total


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product_id = models.PositiveIntegerField()  # store product PK to avoid tight coupling
    product_name = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    added_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.product_name} x{self.quantity}"
