"""
Django settings for ppn_backend project.

Generated by 'django-admin startproject' using Django 2.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'hk+83s0m6j8(ei)gxgy)e59b@^n77y_bmd4(#yyknr#whcrf^#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ENABLE_DEBUG_TOOLBAR = True

ALLOWED_HOSTS = []

INTERNAL_IPS = ['127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'axes',

    # Django extensions
    'django_extensions',

    # django-simple-menu
    'menu',

    # DRF
    'rest_framework',

    # local apps
    'uil.core',
    'uil.vue',
    'api',
    'api.auth',
    'main',
    'experiments',
    'leaders',
    'participants',
    'comments',
    'auditlog',
    'datamanagement',

    'django.contrib.admin',

    # Temp
    'migrate_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'axes.middleware.AxesMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'uil.core.middleware.ThreadLocalUserMiddleware',
    'csp.middleware.CSPMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesBackend',
    'django.contrib.auth.backends.ModelBackend',
]

if DEBUG and ENABLE_DEBUG_TOOLBAR:
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware', )

ROOT_URLCONF = 'ppn_backend.urls'

TEMPLATES = [
    {
        'BACKEND':  'django.template.backends.django.DjangoTemplates',
        'DIRS':     [],
        'APP_DIRS': True,
        'OPTIONS':  {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ppn_backend.wsgi.application'

AUTH_USER_MODEL = 'main.User'

LOGIN_URL = reverse_lazy('main:login')

LOGIN_REDIRECT_URL = reverse_lazy('main:home')

SESSION_COOKIE_NAME = "sessionid_admin"

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'api.permissions.IsPermittedClient',
    )
}

REST_PERMITTED_CLIENTS = ['127.0.0.1']

# Either RSA512 or HS512
JWT_ALGORITHM = 'HS512'

FIELD_ENCRYPTION_KEY = 'IhWBKI5MORNNtI5WWqZwOflEwojBACtuz9lKXwcF4HI='

FRONTEND_URI = 'http://localhost:8000/'

# Groups

LEADER_GROUP = 'leader'
PARTICIPANT_GROUP = 'participant'

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 2525
EMAIL_FROM = 'T.D.Mees@uu.nl'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME':   os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'auditlog': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME':   os.path.join(BASE_DIR, 'auditlog.sqlite3'),
    },
    'old': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'user': 'exp',
            'password': 'exp',
            'db': 'exp',
        }
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


DATABASE_ROUTERS = [
    'ppn_backend.db_router.DatabaseRouter',
    'ppn_backend.db_router.MigrationAppRouter', # TEMP!
]

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'uil.core.hashers.PBKDF2WrappedMD5PasswordHasher',
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'nl'
LANGUAGES = (
    ('nl', _('lang:nl')),
    ('en', _('lang:en')),
)

TIME_ZONE = 'Europe/Amsterdam'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

# Security
# https://docs.djangoproject.com/en/2.0/topics/security/

X_FRAME_OPTIONS = 'DENY'
# Local development server doesn't support https
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_SSL_REDIRECT = not DEBUG

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 60 * 60 * 12  # 12 hours

AXES_LOCKOUT_TEMPLATE = 'main/login_lockout.html'
AXES_RESET_ON_SUCCESS = True
AXES_LOCK_OUT_BY_USER_OR_IP = True
AXES_COOLOFF_TIME = 1

# Django CSP
# http://django-csp.readthedocs.io/en/latest/index.html
CSP_REPORT_ONLY = False
CSP_UPGRADE_INSECURE_REQUESTS = not DEBUG
CSP_INCLUDE_NONCE_IN = ['script-src']

CSP_DEFAULT_SRC = ["'self'", ]
CSP_SCRIPT_SRC = ["'self'", ]
CSP_FONT_SRC = ["'self'", 'data:', ]
CSP_STYLE_SRC = ["'self'", "'unsafe-inline'"]
CSP_IMG_SRC = ["'self'", 'data:', ]

# Django Simple Menu
# https://django-simple-menu.readthedocs.io/en/latest/index.html

MENU_SELECT_PARENTS = True
MENU_HIDE_EMPTY = False

# Auditlog

AUDIT_LOG_ENABLE = True

# try:
#     from .ldap_settings import *
# except ImportError:
#     print('Proceeding without LDAP settings')
