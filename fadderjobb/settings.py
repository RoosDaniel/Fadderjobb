"""
Django settings for fadderjobb project.

Generated by 'django-admin startproject' using Django 2.0.9.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import json
from datetime import date, time

from django.utils import timezone

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

SECRET_KEY_PATH = os.path.join(BASE_DIR, "fadderjobb", "secret_key.txt")

CREDENTIALS_PATH = os.path.join(BASE_DIR, "credentials.json")

if os.path.isfile(SECRET_KEY_PATH):
    with open(SECRET_KEY_PATH) as file:
        SECRET_KEY = file.read()
else:
    from django.utils.crypto import get_random_string

    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    SECRET_KEY = get_random_string(50, chars)

    with open(SECRET_KEY_PATH, "w") as file:
        file.write(SECRET_KEY)

if os.path.isfile(CREDENTIALS_PATH):
    with open(CREDENTIALS_PATH) as file:
        credentials = json.load(file)
else:
    raise FileNotFoundError("No 'credentials.json' found")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", None) == "True"
DEBUG_PROPAGATE_EXCEPTIONS = True

ALLOWED_HOSTS = [
    "localhost",
    "fadderjobb.staben.info",
    "fadderjobb.herokuapp.com",
]

AUTH_USER_MODEL = 'accounts.User'

LOGIN_URL = 'accounts:login'

# Impersonation
# https://github.com/skorokithakis/django-loginas

LOGINAS_LOGOUT_REDIRECT_URL = 'admin:index'
LOGINAS_MESSAGE_LOGIN_SWITCH = 'Du är nu inloggad som {username} - klicka på "Återgå" för att avsluta sessionen.'
LOGINAS_MESSAGE_LOGIN_REVERT = "Du är nu inloggad som {username} igen."

# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
        'post_office': {
            'level': 'WARNING',
        }
    },
}

# Application definition

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'sass_processor',
    'cas',
    'post_office',
    'constance',
    'constance.backends.database',
    'phonenumber_field',
    'loginas',
    'webpush',
    'fadderanmalan',
    'accounts',
    'trade',
    'topchart',
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
    'cas.middleware.CASMiddleware',
    'accounts.middleware.warn_no_phone_number',
    'accounts.middleware.warn_not_read_guide',
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'cas.backends.CASBackend',
)

ROOT_URLCONF = 'fadderjobb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            "templates",
            "accounts.templates",
            "fadderanmalan.templates",
            "trade.templates",
            "topchart.templates",
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'loginas.context_processors.impersonated_session_status',
                'fadderjobb.context_processors.debug',
            ],
        },
    },
]

WSGI_APPLICATION = 'fadderjobb.wsgi.application'

# CAS
# https://github.com/kstateome/django-cas/

CAS_SERVER_URL = "https://login.liu.se/cas/"
CAS_LOGOUT_COMPLETELY = True
CAS_PROVIDE_URL_TO_LOGOUT = True
CAS_RESPONSE_CALLBACKS = [
    'accounts.cas_callbacks.add_email',
    'accounts.cas_callbacks.set_admin',
]

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.environ.get("DB_ENGINE", "django.db.backends.postgresql_psycopg2"),
        'NAME': os.environ.get("DB_NAME", "fadderjobb"),
        'HOST': os.environ.get("DB_HOST", "localhost"),
        'PORT': os.environ.get("DB_PORT", ""),
        'USER': credentials["database"]["user"],
        'PASSWORD': credentials["database"]["user"],
    }
}

# Live settings
# https://github.com/jazzband/django-constance/

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

CONSTANCE_CONFIG = {
    'DEFAULT_JOB_HIDDEN_AFTER': (date(timezone.now().year + 1, 1, 1), 'EFTER detta datum kommer jobben att döljas. '
                                                                      'Kan ändras per jobb.'),
    'DEFAULT_JOB_HIDDEN_UNTIL': (date(timezone.now().year, 1, 1), 'Jobben kommer att visas PÅ detta datum. '
                                                                  'Kan ändras per jobb.'),
    'DEFAULT_JOB_LOCKED_AFTER': (date(timezone.now().year + 1, 1, 1), 'EFTER detta datum kommer jobben att låsas. '
                                                                      'Kan ändras per jobb.'),
    'DEFAULT_JOB_LOCKED_UNTIL': (date(timezone.now().year, 1, 1), 'Jobben kommer att låsas upp PÅ detta datum. '
                                                                  'Kan ändras per jobb.'),
    'DEFAULT_JOB_TIME_END': (time(23, 59, 59), 'När på dagen jobben ska sluta. '
                                               'Kan ändras per jobb.'),
    'DEFAULT_JOB_TIME_START': (time(0, 0, 0), 'När på dagen jobben ska börja. '
                                              'Kan ändras per jobb.'),
    'INFO_MAIL': ("""Hej {user__username}!

Här kommer en länk till extrainformation för jobbet "{job__name}" som du har registrerat dig till:

{job__extra_info}

Jobbet hittar du här:

{job__url}""", 'Infomail. Om jobbet har extra info definerat kommer mailet skickas ut direkt när en användare'
               'registrerar sig, annars kan det skickas ut manuellt genom admin-panelen.'),
    'MIN_POINTS': (0, 'Minsta antalet poäng som krävs av en fadder. Fyller i dagsläget ingen funktionalitet.'),
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    }
]

# Email
# https://docs.djangoproject.com/en/2.1/topics/email/

EMAIL_BACKEND = 'post_office.EmailBackend'

EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")

EMAIL_PORT = os.environ.get("EMAIL_PORT", 587)

EMAIL_HOST_USER = credentials["email"]["user"]

EMAIL_HOST_PASSWORD = credentials["email"]["password"]

EMAIL_USE_TLS = True

POST_OFFICE = {
    "LOG_LEVEL": 0,  # Log nothing
}

try:
    import uwsgidecorators
except ImportError:
    POST_OFFICE["DEFAULT_PRIORITY"] = "now"

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Phone number
# https://github.com/stefanfoulis/django-phonenumber-field/

PHONENUMBER_DEFAULT_REGION = "SE"

# Used by CAS to set admin-status

SYSTEM_ADMINS = [
    "danro880",
    "felfl076",
    "alban042",
]

DEFAULT_DOMAIN = "https://fadderjobb.staben.info"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "fadderjobb", "static"),
    os.path.join(BASE_DIR, "fadderanmalan", "static"),
    os.path.join(BASE_DIR, "accounts", "static"),
    os.path.join(BASE_DIR, "trade", "static"),
    os.path.join(BASE_DIR, "topchart", "static"),
)

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
]

# Webpush
# https://github.com/safwanrahman/django-webpush

WEBPUSH_SETTINGS = credentials["webpush"]
