import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- LOAD ENVIRONMENT VARIABLES FROM .ENV ---
load_dotenv(BASE_DIR / ".env")

# --- AUTOMATED ENVIRONMENT & DEBUG SWITCH ---
IS_LOCAL = os.environ.get("IS_LOCAL", "True").lower() in ("true", "1", "t")
DEBUG = os.environ.get("DEBUG", str(IS_LOCAL)).lower() in ("true", "1", "t")

# Secret key loaded dynamically from environment
SECRET_KEY = os.environ.get("SECRET_KEY", os.environ.get("DJANGO_SECRET_KEY", "django-insecure-b0mep2c1(5s6jofrphgxx2mw0sd9ckgg3nj=1v6da54)gs41=)"))

if IS_LOCAL:
    ALLOWED_HOSTS = ["*"]
    CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1:8000", "http://localhost:8000"]
else:
    allowed_hosts_env = os.environ.get("ALLOWED_HOSTS", "mwirioldboys.com,www.mwirioldboys.com,187.7.19.28,187.77.176.70,localhost,127.0.0.1")
    ALLOWED_HOSTS = [h.strip() for h in allowed_hosts_env.split(",") if h.strip()]

    csrf_origins_env = os.environ.get("CSRF_TRUSTED_ORIGINS", "https://mwirioldboys.com,https://www.mwirioldboys.com,http://mwirioldboys.com,http://www.mwirioldboys.com,http://187.7.19.28,http://187.77.176.70")
    CSRF_TRUSTED_ORIGINS = [o.strip() for o in csrf_origins_env.split(",") if o.strip()]

    # Production Hardening Security Flags
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"
    SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # Third-party apps
    "crispy_forms",
    "crispy_bootstrap5",

    # Local apps
    'core.apps.CoreConfig',
    'users.apps.UsersConfig',
    'pages.apps.PagesConfig',
    'connect.apps.ConnectConfig',
    'organisation.apps.OrganisationConfig',
    'content.apps.ContentConfig',
    'gallery.apps.GalleryConfig',
    'products.apps.ProductsConfig',
    'alumni_sos.apps.AlumniSosConfig',
    'elections.apps.ElectionsConfig',
    'teaser.apps.TeaserConfig',
    'custom_admin.apps.CustomAdminConfig',
    'payments.apps.PaymentsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'moba.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'moba.wsgi.application'


# --- DATABASE SELECTION ---
if IS_LOCAL:
    # LAPTOP: SQLite
    DATABASES = {
        'default': {
            'ENGINE': os.environ.get("DB_ENGINE", "django.db.backends.sqlite3"),
            'NAME': BASE_DIR / "db.sqlite3",
        }
    }
else:
    # VPS: PostgreSQL (Loaded strictly from .env environment variables)
    DATABASES = {
        'default': {
            'ENGINE': os.environ.get("DB_ENGINE", os.environ.get("DATABASE_ENGINE", "django.db.backends.postgresql")),
            'NAME': os.environ.get("DATABASE_NAME", os.environ.get("DB_NAME", "moba_db")),
            'USER': os.environ.get("DATABASE_USER", os.environ.get("DB_USER", "moba_user")),
            'PASSWORD': os.environ.get("DATABASE_PASSWORD", os.environ.get("DB_PASSWORD")),
            'HOST': os.environ.get("DATABASE_HOST", os.environ.get("DB_HOST", "localhost")),
            'PORT': os.environ.get("DATABASE_PORT", os.environ.get("DB_PORT", "5432")),
        }
    }


# Password validation & Reset Timeout
AUTH_PASSWORD_VALIDATORS = []
PASSWORD_RESET_TIMEOUT = 900  # 15 minutes token expiration

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# --- STATIC & MEDIA FILES ---
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Upload size limits (120MB)
DATA_UPLOAD_MAX_MEMORY_SIZE = 125829120  # 120MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 125829120  # 120MB

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Custom User Model & Auth Backends
AUTH_USER_MODEL = 'users.User'
AUTHENTICATION_BACKENDS = [
    'users.backends.CaseInsensitiveModelBackend',
]

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'my_account'

DEFAULT_CURRENCY = 'UGX'
# Admin 2FA Google Authenticator secret key
ADMIN_2FA_SECRET_KEY = os.environ.get('ADMIN_2FA_SECRET_KEY', 'R4R2DVFXBJOCK74JVSK5EBQPIU2MWTYX')