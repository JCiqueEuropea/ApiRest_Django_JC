import os
from pathlib import Path

import environ

env = environ.Env()

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('API_KEY_SECRET', default='django-insecure-key')
DEBUG = env('ENVIRONMENT') == 'development'
ALLOWED_HOSTS = ['*']
LOG_LEVEL = env('LOG_LEVEL', default='INFO')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_spectacular',
    'app',
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

ROOT_URLCONF = 'ApiRest_Django_JC.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages'
        ]},
    },
]

WSGI_APPLICATION = 'ApiRest_Django_JC.wsgi.application'
ASGI_APPLICATION = 'ApiRest_Django_JC.asgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': env('DB_NAME'),
        'HOST': env('DB_HOST'),
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
            'trusted_connection': 'True',
        },
    }
}

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'app.utils.custom_exception_handler',
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES': [
        'app.api.permissions.HasAPIKey',
    ],
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Users & Spotify API',
    'DESCRIPTION': 'Migración de FastAPI a Django',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SECURITY': [{'ApiKeyAuth': []}],
    'APPEND_COMPONENTS': {
        'securitySchemes': {
            'ApiKeyAuth': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'x-api-key',
                'description': 'Enter your API Key Secret'
            }
        }
    }
}

SPOTIFY_CLIENT_ID = env('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = env('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = env('SPOTIFY_REDIRECT_URI')

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
