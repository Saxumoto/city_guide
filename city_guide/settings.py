import os
from pathlib import Path
from decouple import config, Csv
import dj_database_url # NEW: Import the helper library

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# --- CRITICAL DJANGO SETTINGS ---
# Reads SECRET_KEY from the .env file for security
SECRET_KEY = config('SECRET_KEY')

# Reads DEBUG flag from the .env file. MUST be False in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# Reads ALLOWED_HOSTS from the .env file (e.g., 'yourdomain.com')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost', cast=Csv())


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Our custom application
    'attractions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'city_guide.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'city_guide.wsgi.application'


# --- DATABASE CONFIGURATION (FINAL FIX) ---
if config('DATABASE_URL', default=None):
    # CRITICAL: For Render, we use the DATABASE_URL environment variable 
    # and the dj_database_url library to parse it correctly.
    DATABASES = {
        'default': dj_database_url.config(
            default=config('DATABASE_URL'),
            conn_max_age=600,
            conn_health_check=True,
        )
    }
else:
    # Use local SQLite settings if DATABASE_URL is not defined (for local development)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# --- STATIC FILES CONFIGURATION (CSS/JS/etc.) ---
# The URL to serve static files from (production)
STATIC_URL = '/static/'
# The directory where `collectstatic` will output all static files (production deployment)
STATIC_ROOT = BASE_DIR / 'staticfiles'


# --- MEDIA FILES CONFIGURATION (User Uploads) ---
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- AUTH REDIRECTS ---
LOGIN_REDIRECT_URL = '/attractions/'
LOGOUT_REDIRECT_URL = '/accounts/login/'
LOGIN_URL = '/accounts/login/'