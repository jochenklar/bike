# -*- encoding: utf-8 -*-
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'this is not a very secret key'

DEBUG = False

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['localhost']

INTERNAL_IPS = ('127.0.0.1',)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tracks'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware'
)

ROOT_URLCONF = 'bike.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates/')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages'
            ],
        },
    },
]

WSGI_APPLICATION = 'bike.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

LANGUAGE_CODE = 'de-de'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_root/')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root/')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static/'),
)

LOGIN_URL = '/'

TILES_URL = 'https://{s}.tile.thunderforest.com/outdoors/{z}/{x}/{y}.png'
TILES_OPT = {
    'attribution': 'Map tiles by <a href="http://www.thunderforest.com">Thunderforest</a>. Map data by <a href="http://www.openstreetmap.org/copyright">OpenStreetMap contributors</a>',
    'maxZoom': 18,
    'minZoom': 6,
    'zIndex': 0,
    'reuseTiles': 1
}
TRACK_COLOR = '#c06'

# try override with local configuration
try:
    from .local import *
except ImportError:
    pass
