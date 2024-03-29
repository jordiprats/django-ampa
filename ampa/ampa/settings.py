import os

from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-danger',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'd41d8cd98f00b2048cd98f00b204e9800998ecf98f00b204e9800998ecf8427e')

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default':
    {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_NAME', 'ampa'),
        'USER': os.getenv('DB_USER', 'ampa'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'sha1'),
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# SECURITY WARNING: don't run with debug turned on in production!
if os.getenv('DEBUG', False):
    DEBUG=True
else:
    DEBUG=False

PROTOCOL = os.getenv('PROTOCOL', 'http')

ALLOWED_HOSTS = [ os.getenv('PUBLIC_HOSTNAME', 'ampa') ]

if DEBUG:
    ALLOWED_HOSTS += ['localhost', '127.0.0.1']

AUTH_USER_MODEL = 'cole.User'

LOGIN_URL = '/login'
LOGOUT_REDIRECT_URL = '/login/'

XLS_URL = '/xls/'
XLS_ROOT = os.path.join(BASE_DIR, 'xls')

UPLOADS_URL = 'static/uploads'
UPLOADS_ROOT = os.path.join(BASE_DIR, UPLOADS_URL)

USE_TZ = True
TIME_ZONE = 'Europe/Paris'

EMAIL_HOST = os.getenv('EMAIL_HOST', '127.0.0.1')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'demo@localhost')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 'sha1')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))

if os.getenv('EMAIL_USE_TLS', False):
    EMAIL_USE_TLS=True
else:
    EMAIL_USE_TLS=False


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'django.contrib.humanize',
    'django_prometheus',
    'cole',
    'voting',
    'peticions'
]

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware'
]

ROOT_URLCONF = 'ampa.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'templates'
        ],
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

WSGI_APPLICATION = 'ampa.wsgi.application'


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

AUTHENTICATION_BACKENDS = (
    'cole.backends.EmailBackend',
)

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_FULLPATH = os.path.join(BASE_DIR, "static")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATIC_URL = '/static/'

STATIC_DOMAIN = PROTOCOL + '://'+os.getenv('STATIC_HOSTNAME', 'ampa')+'/'

PUBLIC_DOMAIN = PROTOCOL + '://'+os.getenv('PUBLIC_HOSTNAME', 'ampa')

#
#
#

AMPA_DEFAULT_FROM = os.getenv('AMPA_DEFAULT_FROM', 'Demo <email@example.com>')