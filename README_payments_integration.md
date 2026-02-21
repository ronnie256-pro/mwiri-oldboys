This folder documents the payments integration scaffold added to the project.

What was added
- A new Django app `payments` with models: Payment, Cart, CartItem
- Admin registrations for easy management
- Views and templates for cart, checkout, and subscription initiation
- Placeholder webhook and callback handlers for Flutterwave

Next steps to integrate Flutterwave
1. Install requests: pip install requests
2. Add the following environment variables to your environment or .env and ensure they are available in Django settings:
   - FLW_SECRET_KEY (your Flutterwave secret key)
   - FLW_PUBLIC_KEY (your Flutterwave public key)
   - FLW_ENCRYPTION_KEY (optional, for additional security)
   - FLW_SECRET_HASH (if using webhook signature verification)
3. In settings.py add these lines (use os.environ or django-environ):
   FLW_SECRET_KEY = os.environ.get('FLW_SECRET_KEY')
   FLW_PUBLIC_KEY = os.environ.get('FLW_PUBLIC_KEY')
   FLW_BASE_URL = 'https://api.flutterwave.com/v3'

4. Implement the actual HTTP requests in payments.views.checkout (or a separate service module):
   - POST /payments to create a hosted payment (see Flutterwave docs)
   - Verify payments using /transactions/verify endpoint
   - Verify webhook signatures using the FLW_SECRET_HASH

5. Run migrations:
   python manage.py makemigrations payments
   python manage.py migrate

Security notes
- Never commit secret keys. Use environment variables or a secrets manager.
- Use HTTPS for callback/webhook endpoints in production.
