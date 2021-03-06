"""
Django settings for activationsapi project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
import os
from config import configuration as conf

SECRET_KEY = conf.SECRET_KEY

DEBUG = conf.DEBUG

ALLOWED_HOSTS = conf.ALLOWED_HOSTS


# Application definition

INSTALLED_APPS = [
    "activation.apps.SuitConfig",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'corsheaders',

    'activation.apps.ActivationConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # CORS middleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = ["https://activations.xyz"]

ROOT_URLCONF = 'activationsapi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(conf.BASE_DIR, 'templates'),],
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

WSGI_APPLICATION = 'activationsapi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': conf.DBNAME,
        'USER': conf.DBUSER,
        'PASSWORD': conf.DBPASSWORD,
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'CONN_MAX_AGE': 5,
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'activation.User'

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = conf.STATIC_ROOT
STATIC_URL = conf.STATIC_URL
MEDIA_ROOT = conf.MEDIA_ROOT
MEDIA_URL = conf.MEDIA_URL
# DigitalOcean Spaces Configuration
# ==================================

AWS_ACCESS_KEY_ID = conf.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = conf.AWS_SECRET_ACCESS_KEY
AWS_STORAGE_BUCKET_NAME = 'proximityrentals'
AWS_S3_REGION_NAME = 'sfo2'
AWS_S3_ENDPOINT_URL = 'https://sfo2.digitaloceanspaces.com'
AWS_S3_CUSTOM_DOMAIN = 'cdn.billstack.net'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_S3_SECURE_URLS = True
AWS_PUBLIC_MEDIA_LOCATION = 'avtn/media/'
AWS_PREVIEW_IMAGE_LOCATION = os.path.join(AWS_PUBLIC_MEDIA_LOCATION, 'software/')
AWS_DEFAULT_ACL = 'public-read'
