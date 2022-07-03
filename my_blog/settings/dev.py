from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'lmvn^7z=z93fo2boh1q9192j2i&7(xgpy)^_zsmry(0wy7a$pv'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

BASE_DIR = os.getcwd()

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SERVER_EMAIL = 'test@my_blog.com'
DEFAULT_FROM_EMAIL = SERVER_EMAIL

ADMINS = [
    ('KTeam', 'test@resend.com'),
]

MANAGERS = ADMINS

