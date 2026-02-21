from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/update/', views.update_cart, name='update_cart_item'),
    path('cart/remove/', views.remove_from_cart, name='remove_cart_item'),
    path('checkout/', views.checkout, name='checkout'),

    path('subscribe/', views.subscribe_view, name='subscribe'),
    path('subscribe/initiate/', views.initiate_subscription_payment, name='initiate_subscription_payment'),
]
