import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'tahJeLot9Keib9Iehofi6ef3eewaeM9shiL1zeeWe8id2ahief2shaecai3Phoom'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['bike.jochenklar.de']

ADMINS = (
    ('Jochen Klar', 'admin@jochenklar.de'),
)

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
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'bike.urls'

WSGI_APPLICATION = 'bike.wsgi.application'

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'bike',
    #     'USER': 'bike',
    #     'PASSWORD': 'bike',
    #     'HOST': 'localhost',
    #     'PORT': '',
    # }
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/bike.db'
    }
}

LANGUAGE_CODE = 'de-de'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = os.path.join(BASE_DIR,'media/')

MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR,'static/')

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR,'bike/static/'),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'bike/templates'),
    os.path.join(BASE_DIR, 'tracks/templates'),
)

LOGIN_URL = '/'
