"""
Django settings for recod_admin project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')ima!obvl-lazqeq$brkb9!g0ihdi_eg^+y1e)@8_1^&8s*rkh'

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
    'competition',
    'account',
    'article',
    'video',
    'cms',
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

ROOT_URLCONF = 'recod_admin.urls'

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

WSGI_APPLICATION = 'recod_admin.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/recod_admin/staticfiles'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

DATABASE_ROUTERS = ['recod_admin.dbrouters.DefaultDBRouter']

# Logging
LOGGING_PREFIX = 'recod_admin'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            '()': 'colorlog.ColoredFormatter',
            'format': ('%(log_color)s[%(levelname)s]'
                       '[in %(pathname)s:%(lineno)d]'
                       '%(asctime)s %(process)d %(thread)d '
                       '%(module)s: %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'log_colors': {
                'DEBUG':    'bold_black',
                'INFO':     'white',
                'WARNING':  'yellow',
                'ERROR':    'red',
                'CRITICAL': 'bold_red',
            },
        },
        'sql': {
            '()': 'colorlog.ColoredFormatter',
            'format': '%(cyan)s[SQL] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'syslog_verbose': {
            'format': ('{}:[%(levelname)s] [in %(pathname)s:%(lineno)d] '
                       '%(asctime)s %(process)d %(thread)d '
                       '%(module)s: %(message)s'.format(LOGGING_PREFIX)),
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        # コンソール出力するハンドラ
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        # SQLをコンソール出力するハンドラ
        'sql': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'sql'
        },
        # null出力するハンドラ
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
    },
    'loggers': {
        # djangoのログ
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        },
        # Database Query
        'django.db.backends': {
            'handlers': ['sql'],
            'level': 'DEBUG',
            'propagate': False,
        },
        LOGGING_PREFIX: {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

try:
    from .database import *
    from .static_settings import *
except ImportError:
    raise

