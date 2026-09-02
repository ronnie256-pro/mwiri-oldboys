class SecurityHeadersMiddleware:
    """
    Middleware that adds production HTTP Security Headers:
    - Strict-Transport-Security (HSTS)
    - Content-Security-Policy (CSP)
    - Permissions-Policy
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # 1. HSTS (Strict-Transport-Security)
        response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'

        # 2. Permissions-Policy
        response['Permissions-Policy'] = 'camera=(), microphone=(), geolocation=(), payment=()'

        # 3. Content-Security-Policy (Allows self, Bootstrap CDNs, Google Fonts, and images)
        response['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; "
            "font-src 'self' https://cdn.jsdelivr.net https://fonts.gstatic.com data:; "
            "img-src 'self' data: https: http: blob:; "
            "connect-src 'self'; "
            "frame-ancestors 'none';"
        )

        return response
