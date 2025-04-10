"""
Django settings for urbanflow project.

Generated by 'django-admin startproject' using Django 5.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

# transit_project/settings.py
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-tln+r&^9=yi%cu$up6i^o7cff=_*@jw@hmp#9u-_vnb+2h!u=p'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'base.apps.BaseConfig',
    'corsheaders',
    'base.tranzy_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'urbanflow.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR/ 'templates'
        ],
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

WSGI_APPLICATION = 'urbanflow.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CORS_ALLOW_ALL_ORIGINS = True
ALLOWED_HOSTS = ['192.168.0.153', 'localhost', '127.0.0.1']


NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")


TRANZY_BASE_URL = os.getenv('TRANZY_BASE_URL', 'https://api.tranzy.ai/v1/opendata')
TRANZY_API_KEY = os.getenv('TRANZY_API_KEY', '')


TRANZY_AGENCY_MAPPING = {
    'Iasi': {
        'agency_id': '1',
        'agency_name': 'SCTP Iasi',
        'agency_url': 'https://www.sctpiasi.ro/',
        'agency_timezone': 'Europe/Bucharest',
        'agency_lang': 'ro',
    },
    'Cluj-Napoca': {
        'agency_id': '2',
        'agency_name': 'CTP Cluj',
        'agency_url': 'https://www.ctpcluj.ro/',
        'agency_timezone': 'Europe/Bucharest',
        'agency_lang': 'ro',
    },
    'Chisinau': {
        'agency_id': '4',
        'agency_name': 'RTEC&PUA Chisinau',
        'agency_url': 'https://www.rtec.md/',
        'agency_timezone': 'Europe/Bucharest',
        'agency_lang': 'ro',
    },
    'Botosani': {
        'agency_id': '6',
        'agency_name': 'Eltrans Botosani',
        'agency_url': 'https://www.eltransbt.ro/',
        'agency_timezone': 'Europe/Bucharest',
        'agency_lang': 'ro',
    },
    'Timisoara': {
        'agency_id': '8',
        'agency_name': 'STPT Timisoara',
        'agency_url': 'https://www.ratt.ro/',
        'agency_timezone': 'Europe/Bucharest',
        'agency_lang': 'ro',
    },
    'Oradea': {
        'agency_id': '9',
        'agency_name': 'OTL Oradea',
        'agency_url': 'https://www.otlra.ro/',
        'agency_timezone': 'Europe/Bucharest',
        'agency_lang': 'ro',
    },
}