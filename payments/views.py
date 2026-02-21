import json
import uuid
from decimal import Decimal
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Cart, CartItem, Payment
from django.contrib.auth.decorators import login_required
from django.urls import reverse


@login_required
@require_POST
def add_to_cart(request):
    data = json.loads(request.body.decode('utf-8')) if request.body and request.content_type == 'application/json' else request.POST
    product_id = data.get('product_id')
    price = data.get('price')
    name = data.get('name')
    qty = int(data.get('quantity', 1))

    if not product_id or not price:
        return HttpResponseBadRequest('product_id and price are required')

    price = Decimal(price)

    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product_id=product_id, defaults={'price': price, 'product_name': name or ''})
    if not created:
        item.quantity += qty
        item.price = price
        item.save()

    # If request is AJAX/JSON, return JSON. Otherwise redirect to cart page for progressive enhancement.
    is_ajax = (request.headers.get('x-requested-with') == 'XMLHttpRequest') or (request.content_type == 'application/json')
    if is_ajax:
        return JsonResponse({'status': 'ok', 'cart_total': str(cart.total_amount())})

    return redirect('payments:view_cart')


@login_required
def view_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    return render(request, 'payments/cart.html', {'cart': cart})


@login_required
@require_POST
def update_cart(request):
    data = json.loads(request.body.decode('utf-8')) if request.body and request.content_type == 'application/json' else request.POST
    product_id = data.get('product_id')
    qty = int(data.get('quantity', 0))

    if qty <= 0:
        return HttpResponseBadRequest('Quantity must be greater than 0')

    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(CartItem, cart=cart, product_id=product_id)

    item.quantity = qty
    item.save()

    # If request is AJAX/JSON, return JSON. Otherwise redirect to cart page for progressive enhancement.
    is_ajax = (request.headers.get('x-requested-with') == 'XMLHttpRequest') or (request.content_type == 'application/json')
    if is_ajax:
        return JsonResponse({'status': 'ok', 'cart_total': str(cart.total_amount())})

    return redirect('payments:view_cart')


@login_required
@require_POST
def remove_from_cart(request):
    data = json.loads(request.body.decode('utf-8')) if request.body and request.content_type == 'application/json' else request.POST
    product_id = data.get('product_id')

    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    item.delete()

    # If request is AJAX/JSON, return JSON. Otherwise redirect to cart page for progressive enhancement.
    is_ajax = (request.headers.get('x-requested-with') == 'XMLHttpRequest') or (request.content_type == 'application/json')
    if is_ajax:
        return JsonResponse({'status': 'ok', 'cart_total': str(cart.total_amount())})

    return redirect('payments:view_cart')


@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    # calculate total and provide a lightweight payment object for the template
    total = cart.total_amount()
    tx_ref = f"cart_{uuid.uuid4().hex}"
    payment = {'amount': total, 'tx_ref': tx_ref}

    if request.method == 'POST':
        # Handle the checkout process (integration with Flutterwave will be implemented later)
        return JsonResponse({'status': 'ok'})

    return render(request, 'payments/checkout.html', {'cart': cart, 'payment': payment})


def cart_total(request):
    if request.user.is_authenticated:
        cart = get_object_or_404(Cart, user=request.user)
        total = cart.total_amount()
    else:
        total = 0

    return JsonResponse({'total': str(total)})


@csrf_exempt
def create_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        amount = data.get('amount')
        currency = data.get('currency', 'usd')
        payment_method = data.get('payment_method')
        receipt_email = data.get('receipt_email')

        if not amount or not payment_method:
            return HttpResponseBadRequest('Amount and payment_method are required')

        try:
            # Create a PaymentIntent with the order amount and currency
            payment_intent = PaymentIntent.create(
                amount=int(amount * 100),  # Amount in cents
                currency=currency,
                payment_method=payment_method,
                confirmation_method='manual',
                confirm=True,
                metadata={'user_id': request.user.id}
            )

            # Save the payment details in the database
            Payment.objects.create(
                user=request.user,
                amount=amount,
                currency=currency,
                payment_method=payment_method,
                status=payment_intent['status'],
                receipt_email=receipt_email
            )

            return JsonResponse({'status': 'success', 'payment_intent': payment_intent['id']})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


def subscribe_view(request):
    from django.shortcuts import render

    options = [
        {"label": "Annual Subscription", "amount": 50000, "key": "annual"},
        {"label": "Lifetime Membership", "amount": 1010000, "key": "lifetime"},
    ]

    return render(request, "payments/subscribe.html", {"options": options})


@login_required
@require_POST
def initiate_subscription_payment(request):
    data = json.loads(request.body.decode('utf-8')) if request.body and request.content_type == 'application/json' else request.POST
    option = data.get('option') or data.get('plan')
    if option not in ['annual', 'lifetime']:
        return HttpResponseBadRequest('invalid option')

    amount = Decimal('50000.00') if option == 'annual' else Decimal('1010000.00')
    tx_ref = f"sub_{uuid.uuid4().hex}"

    payment = Payment.objects.create(
        user=request.user,
        tx_ref=tx_ref,
        amount=amount,
        currency=getattr(settings, 'DEFAULT_CURRENCY', 'UGX'),
        status=Payment.STATUS_PENDING,
        email=request.user.email,
        name=getattr(request.user, 'get_full_name', lambda: '')() or request.user.username,
        metadata={'subscription_type': option},
    )

    # Add subscription as a cart item so user can review/checkout from the cart page
    cart, _ = Cart.objects.get_or_create(user=request.user)
    product_name = 'MOBA Subscription - Annual' if option == 'annual' else 'MOBA Subscription - Lifetime'
    CartItem.objects.update_or_create(
        cart=cart,
        product_id=0,
        defaults={'price': amount, 'product_name': product_name, 'quantity': 1}
    )

    cart_url = reverse('payments:view_cart')
    is_ajax = (request.headers.get('x-requested-with') == 'XMLHttpRequest') or (request.content_type == 'application/json')
    if is_ajax:
        return JsonResponse({'status': 'ok', 'tx_ref': tx_ref, 'amount': str(amount), 'cart_url': cart_url})

    return redirect(cart_url)
