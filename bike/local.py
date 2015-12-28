DEBUG = True

SECRET_KEY = 'tief5yoh8aerootoh2tohThah0giroemoo5AiGe6Ooh4oojeejaT4jo4voca9ahk'

ALLOWED_HOSTS = ['localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'bike',
        'USER': 'bike',
    }
}
