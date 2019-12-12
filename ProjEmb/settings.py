import os
import django_heroku
import redis
from celery.schedules import crontab
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# DISCLAIMER: If you are to locally develop this codebase follow these instructions:
# 1. Set debug = os.getenv('DEBUG_STATUS', True )
# 2. Set celery_broker and celery_result to the development options,
# 3. Don't set compress_offline = True or you'll regret it in production
# 4. run python manage.py collectstatic if you altered static files
# 6. Push to Heroku
# @@@@--- This is essential for the production site. ---@@@

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG_STATUS', False)

# Celery
# For Development and local Redis server
# CELERY_BROKER_URL = 'redis://localhost:6379'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379'

# For Production
CELERY_BROKER_URL = os.environ['REDIS_URL']
CELERY_RESULT_BACKEND = os.environ['REDIS_URL']


ALLOWED_HOSTS = ['https://pe-resource-platform.herokuapp.com/']
# Application definition
LOGIN_URL = '/login/'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django_celery_results',
    'inventory',
    'simple_pagination',
    'bootstrap3',
    'bootstrap4',
    'crispy_forms',
    "django_filters",
    "django_tables2",
    'compressor',
    'haystack',
    'common',
    'accounts',
    'cases',
    'contacts',
    'emails',
    'leads',
    'opportunity',
    'planner',
    'sorl.thumbnail',
    'phonenumber_field',
    'storages',
    'marketing',
    'tasks',
    'invoices',
    'events',
    'teams',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'ProjEmb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates"), ],
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

WSGI_APPLICATION = 'ProjEmb.wsgi.application'

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Eastern'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Sets date format for models
DATE_INPUT_FORMATS = ['%d-%m-%Y']

django_heroku.settings(locals())

# BEGIN DJANGO-CRM Settings ----------------------------------------------------------------

EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'

AUTH_USER_MODEL = 'common.User'

# The following configuration is key for Heroku.
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

STORAGE_TYPE = os.getenv('STORAGE_TYPE', 's3-storage') # Either normal or s3-storage

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"), ]
STATIC_URL = '/static/'

if STORAGE_TYPE == 'normal':
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'

    STATIC_URL = '/static/'
    STATICFILES_DIRS = (BASE_DIR + '/static/',)
    COMPRESS_ROOT = BASE_DIR + '/static/'

# AWS was not utilized due to costs. If you would like to utilize media files and profile pictures you will need to
# implement AWS file storage and route the application to the AWS AWS_BUCKET_NAME
elif STORAGE_TYPE == 's3-storage':

    AWS_STORAGE_BUCKET_NAME = AWS_BUCKET_NAME = os.getenv('AWSBUCKETNAME', 'pe-resource-media')
    AM_ACCESS_KEY = AWS_ACCESS_KEY_ID = os.environ.get('AKIAI5CFRK4IEWBOSMWQ')
    AM_PASS_KEY = AWS_SECRET_ACCESS_KEY = os.environ.get('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')
    S3_DOMAIN = AWS_S3_CUSTOM_DOMAIN = str(AWS_BUCKET_NAME) + '.s3.amazonaws.com' # us-east-ohio

    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }

    # STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    DEFAULT_S3_PATH = 'media'
    # STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    # STATIC_S3_PATH = "static"
    # COMPRESS_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    #
    # COMPRESS_CSS_FILTERS = [
    #     'compressor.filters.css_default.CssAbsoluteFilter', 'compressor.filters.cssmin.CSSMinFilter']
    # COMPRESS_JS_FILTERS = ['compressor.filters.jsmin.JSMinFilter']
    # COMPRESS_REBUILD_TIMEOUT = 5400

    MEDIA_ROOT = '/%s/' % DEFAULT_S3_PATH
    MEDIA_URL = '//%s/%s/' % (S3_DOMAIN, DEFAULT_S3_PATH)
    # STATIC_ROOT = "/%s/" % STATIC_S3_PATH
    # STATIC_URL = 'https://%s/' % (S3_DOMAIN)
    # ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

    CORS_ORIGIN_ALLOW_ALL = True

    AWS_IS_GZIPPED = True
    AWS_ENABLED = True
    AWS_S3_SECURE_URLS = True
    AWS_DEFAULT_ACL = None

COMPRESS_ROOT = BASE_DIR + '/static/'

COMPRESS_ENABLED = True

COMPRESS_OFFLINE_CONTEXT = {
    'STATIC_URL': 'STATIC_URL',
}

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter', 'compressor.filters.cssmin.CSSMinFilter']
COMPRESS_REBUILD_TIMEOUT = 5400

COMPRESS_OUTPUT_DIR = 'CACHE'
COMPRESS_URL = STATIC_URL

COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
    ('text/x-sass', 'sass {infile} {outfile}'),
    ('text/x-scss', 'sass {infile} {outfile}'),
)

COMPRESS_OFFLINE_CONTEXT = {
    'STATIC_URL': 'STATIC_URL',
}

DEFAULT_FROM_EMAIL = 'proememails@gmail.com'


# Load the local settings file if it exists
if os.path.isfile('ProjEmb/local_settings.py'):
    from .local_settings import *
else:
    print("No local settings file found")

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'proememails@gmail.com'
EMAIL_HOST_PASSWORD = 'meohvgatpjcdrnyt'

PASSWORD_RESET_MAIL_FROM_USER = os.getenv('PASSWORD_RESET_MAIL_FROM_USER', 'proememails@gmail.com')

MAIL_SENDER = 'GOOGLE'

try:
    from .dev_settings import *
except ImportError:
    pass

# For Local host http://127.0.0.1:8000/
# GP_CLIENT_ID = os.getenv('GP_CLIENT_ID', '260552032070-vfh4keifnnnou3f5v9uj7jrk4a67t257.apps.googleusercontent.com')
# GP_CLIENT_SECRET = os.getenv('GP_CLIENT_SECRET', 'qYkKQy42MOWVuITtyO14Hnd2')
# ENABLE_GOOGLE_LOGIN = os.getenv('ENABLE_GOOGLE_LOGIN', True)

# Was unable to make this work with Heroku, but these are the tokens required. Check googleAPI for credentials.
GP_CLIENT_ID = os.getenv('GP_CLIENT_ID', 'SECRETSECRET')
GP_CLIENT_SECRET = os.getenv('GP_CLIENT_SECRET', 'SECRETSECRET')
ENABLE_GOOGLE_LOGIN = os.getenv('ENABLE_GOOGLE_LOGIN', False)


# Items for marketing which are not currently being utilized.

MARKETING_REPLY_EMAIL = 'proememails@gmail.com'

PASSWORD_RESET_TIMEOUT_DAYS = 2

SENTRY_ENABLED = os.getenv('SENTRY_ENABLED', False)

if SENTRY_ENABLED and not DEBUG:
    if os.getenv('SENTRYDSN') is not None:
        RAVEN_CONFIG = {
            'dsn': os.getenv('SENTRYDSN', ''),
        }
        INSTALLED_APPS = INSTALLED_APPS + [
            'raven.contrib.django.raven_compat',
        ]
        MIDDLEWARE = [
            'raven.contrib.django.raven_compat.middleware.Sentry404CatchMiddleware',
            'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
         ] + MIDDLEWARE
        LOGGING = {
            'version': 1,
            'disable_existing_loggers': True,
            'root': {
                'level': 'WARNING',
                'handlers': ['sentry'],
            },
            'formatters': {
                'verbose': {
                    'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
                },
            },
            'handlers': {
                'sentry': {
                    'level': 'ERROR',
                    'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
                },
                'console': {
                    'level': 'DEBUG',
                    'class': 'logging.StreamHandler',
                    'formatter': 'verbose'
                }
            },
            'loggers': {
                'django.db.backends': {
                    'level': 'ERROR',
                    'handlers': ['console'],
                    'propagate': False,
                },
                'raven': {
                    'level': 'DEBUG',
                    'handlers': ['console'],
                    'propagate': False,
                },
                'sentry.errors': {
                    'level': 'DEBUG',
                    'handlers': ['console'],
                    'propagate': False,
                },
            },
        }

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch2_backend.Elasticsearch2SearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
    },
}

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10



# Uncomment this to diagnose issues in a non-debug environment
# Be prepared, this system has a fuckload of logging.
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
#             'datefmt' : "%d/%b/%Y %H:%M:%S"
#         },
#         'simple': {
#             'format': '%(levelname)s %(message)s'
#         },
#     },
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': 'mysite.log',
#             'formatter': 'verbose'
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers':['file'],
#             'propagate': True,
#             'level':'DEBUG',
#         },
#         'MYAPP': {
#             'handlers': ['file'],
#             'level': 'DEBUG',
#         },
#     }

# }
