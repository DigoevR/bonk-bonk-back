"""
Django settings for bonkbonkback project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import dj_database_url
from datetime import timedelta
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-kd(8p(zn*3=dx+(zhj7()m$9h3r#3dw9$a5$s_sairpowbmbwn' if DEBUG else os.environ.get('DJANGO_SECRET')

ALLOWED_HOSTS = ['localhost', 'bonk-bonk.herokuapp.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'channels',
    'knox',
    'sorl.thumbnail',
    'storages',

    'custom_auth.apps.CustomAuthConfig',
    'tennis.apps.TennisConfig',
]

MIDDLEWARE = [
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bonkbonkback.urls'

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
                'django.template.context_processors.media',
            ],
        },
    },
]
ASGI_APPLICATION = 'bonkbonkback.asgi.application'
WSGI_APPLICATION = 'bonkbonkback.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
LOCAL = os.environ.get("DJANGO_IS_LOCAL")
if LOCAL:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASE_URL = os.environ.get('DATABASE_URL')
    DATABASES = {
    'default': dj_database_url.config(),
}
    THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.redis_kvstore.KVStore'
    THUMBNAIL_REDIS_URL = os.environ.get('REDIS_URL')


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
if LOCAL:
    STATIC_URL = '/static/'
    STATIC_ROOT = BASE_DIR / 'static/'

    MEDIA_URL = 'http://localhost:8000/media/'
    MEDIA_ROOT = BASE_DIR / 'media/'
else:
    AWS_ACCESS_KEY_ID = os.environ.get('BUCKETEER_AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('BUCKETEER_AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('BUCKETEER_BUCKET_NAME')
    AWS_S3_REGION_NAME = os.environ.get('BUCKETEER_AWS_REGION')
    AWS_DEFAULT_ACL = None
    # AWS_S3_SIGNATURE_VERSION = os.environ.get('S3_SIGNATURE_VERSION', 's3v4')
    AWS_S3_ENDPOINT_URL = f'https://s3.{AWS_S3_REGION_NAME}.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

    STATIC_DEFAULT_ACL = 'public-read'
    STATIC_LOCATION = 'public/static'
    STATIC_URL = f'{AWS_S3_ENDPOINT_URL}/{STATIC_LOCATION}/'
    STATICFILES_STORAGE = 'utils.storage_backends.StaticStorage'
    PUBLIC_MEDIA_DEFAULT_ACL = 'public-read'
    PUBLIC_MEDIA_LOCATION = 'public/media'

    MEDIA_URL = f'{AWS_S3_ENDPOINT_URL}/{PUBLIC_MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'utils.storage_backends.PublicMediaStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': ['knox.auth.TokenAuthentication',],
}
if DEBUG:
    REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] += ['rest_framework.authentication.SessionAuthentication',]

REST_KNOX = {
  'SECURE_HASH_ALGORITHM': 'cryptography.hazmat.primitives.hashes.SHA512',
  'AUTH_TOKEN_CHARACTER_LENGTH': 64,
  'TOKEN_TTL': timedelta(weeks=8),
  'USER_SERIALIZER': 'custom_auth.serializers.UserSerializer',
  'TOKEN_LIMIT_PER_USER': None,
  'AUTO_REFRESH': False,
}

AUTH_USER_MODEL = 'custom_auth.User'

CSRF_TRUSTED_ORIGINS = ['http://localhost:8000', 'https://bonk-bonk.herokuapp.com']