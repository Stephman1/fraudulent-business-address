"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
import sys

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Define the path to the logs folder
LOG_DIR = os.path.join(BASE_DIR, 'logs')

# Create the logs directory if it doesn't exist
os.makedirs(LOG_DIR, exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'debug_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'debug.log'),
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'error.log'),
            'formatter': 'verbose',
        },
        'views_debug_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'views_debug.log'),
            'formatter': 'verbose',
        },
        'views_error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'views_error.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['debug_file', 'error_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'address.views': {
            'handlers': ['views_debug_file', 'views_error_file'],
            'level': 'DEBUG',
            'propagate': False,  # Prevent duplicate logs in the django logger
        },
    },
} 

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# NOTE: You can generate a new secret key via the following command:
# -> python manage.py shell
# -> from django.core.management.utils import get_random_secret_key
# -> print(get_random_secret_key())
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "server",   # Internal Docker Compose service name for Django
    "client",   # Internal Docker Compose service name for React
    # "your-production-domain.com",  # Replace with your domain in production
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://client:3000",
    "http://localhost:3000",
]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "address.apps.AddressConfig",
    'rest_framework',
    "corsheaders",
    "debug_toolbar",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

INTERNAL_IPS = [
    "127.0.0.1",
    "172.17.0.1",  # Default Docker bridge IP
]



ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': os.getenv('DB_PORT', '5432'),
        'TEST': {
            'NAME': 'test_db',  # Name of the test database
        },
    }
}

# Optionally, you can use an in-memory SQLite database for faster tests
if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# The directory where static files will be collected for production (e.g., running collectstatic)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Directories where Django will look for static files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # Global static folder
    os.path.join(BASE_DIR, 'address/static'),  # Static folder for the 'address' app
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
