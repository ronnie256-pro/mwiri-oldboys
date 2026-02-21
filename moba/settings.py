import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- THE PRODUCTION SWITCH ---
# Keep this as True while working on your laptop.
# IMPORTANT: Change this to False before you commit and push to GitHub!
IS_LOCAL = True

# Quick-start development settings - unsuitable for production
SECRET_KEY = 'django-insecure-b0mep2c1(5s6jofrphgxx2mw0sd9ckgg3nj=1v6da54)gs41=)'

if IS_LOCAL:
    DEBUG = True
    ALLOWED_HOSTS = []
else:
    DEBUG = False
    ALLOWED_HOSTS = ['mwirioldboys.com', 'www.mwirioldboys.com', '147.93.52.129']
    CSRF_TRUSTED_ORIGINS = ['https://mwirioldboys.com', 'https://www.mwirioldboys.com']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    "crispy_forms",
    "crispy_bootstrap5",

    # Local apps
    'core.apps.CoreConfig',
    'users.apps.UsersConfig',
    'pages.apps.PagesConfig',
    'connect.apps.ConnectConfig',
    'content.apps.ContentConfig',
    'products.apps.ProductsConfig',
    'custom_admin.apps.CustomAdminConfig',
    'teaser.apps.TeaserConfig',
    'organisation.apps.OrganisationConfig',
    'alumni_sos.apps.AlumniSosConfig',
    'stories.apps.StoriesConfig',
]

INSTALLED_APPS += [
    'payments',
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
        'DIRS': [BASE_DIR / 'core/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
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
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # VPS: PostgreSQL
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'mwiri_db',
            'USER': 'mwiri_user',
            'PASSWORD': '*@olbboys2026#',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# --- STATIC & MEDIA FILES ---
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Add this line to ensure WhiteNoise handles compression and caching
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Custom User Model
AUTH_USER_MODEL = 'users.User'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'my_account'

DEFAULT_CURRENCY = 'UGX'
# Flutterwave settings placeholders - set these via environment variables
FLW_SECRET_KEY = None
FLW_PUBLIC_KEY = None
FLW_BASE_URL = 'https://api.flutterwave.com/v3'