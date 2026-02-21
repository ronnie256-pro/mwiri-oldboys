from django.contrib import admin
from .models import Payment, Cart, CartItem


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('tx_ref', 'user', 'amount', 'currency', 'status', 'created_at')
    search_fields = ('tx_ref', 'flw_ref', 'user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'cart', 'quantity', 'price', 'added_at')
    search_fields = ('product_name',)
