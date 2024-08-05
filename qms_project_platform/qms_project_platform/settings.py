
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

import os

# ...

if 'DJANGO_ENV' in os.environ and os.environ['DJANGO_ENV'] == 'production':
    BASE_URL = 'https://qmserver.com/'
else:
    BASE_URL = 'http://localhost:8000/'



SECRET_KEY = 'django-insecure-@+x8aq^udl677u-ev_3x%-l$6l945()wmxnm)9+bo#1)onmr#&'


DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1']
CORS_ALLOWED_ORIGINS = [
    'http://localhost',
    'http://127.0.0.1',
    'http://0.0.0.0',
    'http://localhost:3000',
    'http://localhost:8000',
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = ['Content-Type', 'Authorization', 'Algorithm', 'Secret-Key', 'Accept', 'Cache-Control']
CORS_ALLOW_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
CORS_ALLOW_ALL_ORIGINS = True





INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users_app_api',
    'ambulance_app_api',
    'e_consultant_app_api',
    'hospital_app_api',
    'flutterwave_payment_app_api',
    'rest_framework',
    'corsheaders',
    'rest_framework.authtoken',
    'ratelimit',
    'rest_framework_swagger',
    'drf_spectacular',
    'rest_framework_api_key',
    
]




MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]



ROOT_URLCONF = 'qms_project_platform.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'users_app_api', 'templates')],
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

WSGI_APPLICATION = 'qms_project_platform.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}




AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



STATIC_URL = '/static/'



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 
           'drf_spectacular.openapi.AutoSchema',
    
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Quicmed Security API Server Documentation",
}