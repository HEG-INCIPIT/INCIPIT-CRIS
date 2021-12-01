"""
Django settings for INCIPIT_CRIS project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'n(v4*hs62%0*%)p*5f^0w=gl5i_3#i7pqz&%@=$%mvs*h#j1=7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'INCIPIT_CRIS_app.apps.IncipitCrisAppConfig',
    'arketype_API.apps.ArketypeApiConfig',
    'sparql_triplestore.apps.SparqlTriplestoreConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cookiebanner',
]
COOKIEBANNER = {
    "title": "Réglages des cookies",
    "header_text": "Nous utilisons des cookies sur notre site.",
    "footer_text": "Accepter nos cookies, s'il vous plaît.",
    # "footer_links": [
    #     {"title": "Imprint", "href": "/imprint"},
    #     {"title": "Privacy", "href": "/privacy"},
    # ],
    "groups": [
        {
            "id": "essential",
            "name": "Essentiel",
            "description": "Ces cookies essentiels sont nécessaires au fonctionnement du site.",
            "cookies": [
                {
                    "pattern": "cookiebanner",
                    "description": "Meta cookie qui gère les cookies.",
                },
                {
                    "pattern": "csrftoken",
                    "description": "Ce cookie prévient les attaques de type \"Cross-Site-Request-Forgery attacks.\"",
                },
                {
                    "pattern": "sessionid",
                    "description": "Ce cookie sert à la connexion.",
                },
            ],
        }
    ],
}
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'INCIPIT_CRIS.urls'

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

WSGI_APPLICATION = 'INCIPIT_CRIS.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'incipit_cris',
        'USER': 'INCIPIT-CRIS',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

# User model reference
AUTH_USER_MODEL = 'INCIPIT_CRIS_app.User'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

URL = 'http://www.localhost:8000/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

SCHEMA_FILE_NAME = 'schemaorg-20210511.ttl'
SCHEMA_ROOT = os.path.join(BASE_DIR, '')[:-13] + 'schema_ontology/'

FUSEKI_USER = 'admin'
FUSEKI_PASSWORD = 'pw'

# Authetication backend
#AUTHENTICATION_BACKENDS = ['INCIPIT_CRIS_app.authentication.EmailBackend']
