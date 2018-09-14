# -*- encoding: utf-8 -*-
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DEBUG = False

INTERNAL_IPS = ('127.0.0.1',)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'vendor_files',
    'compressor',
    'tracks'
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_root/')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root/')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'vendor/'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder'
)

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

VENDOR = {
    'vue': {
        'url': 'https://cdn.jsdelivr.net/npm/vue@2.5.16/',
        'js': [
            {
                'path': 'dist/vue.min.js',
            }
        ]
    },
    'leaflet': {
        'url': 'https://unpkg.com/leaflet@1.3.3/',
        'js': [
            {
                'path': 'dist/leaflet.js',
                'sri': 'sha512-tAGcCfR4Sc5ZP5ZoVz0quoZDYX5aCtEm/eu1KhSLj2c9eFrylXZknQYmxUssFaVJKvvc0dJQixhGjG2yXWiV9Q==',
            }
        ],
        'css': [
            {
                'path': 'dist/leaflet.css',
                'sri': 'sha512-Rksm5RenBEKSKFjgI3a41vrjkw4EVPlJ3+OiI65vTjIdo9brlAacEuKOiQ5OFh7cOI1bkDwLqdLw3Zg0cRJAAQ==',
            }
        ]
    },
    'Chart': {
        'url': 'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.1/',
        'js': [
            {
                'path': 'Chart.min.js',
            }
        ]
    },
    'vue-chartjs': {
        'url': 'https://unpkg.com/vue-chartjs/',
        'js': [
            {
                'path': 'dist/vue-chartjs.min.js',
            }
        ]
    }
}

# try override with local configuration
from .local import *
