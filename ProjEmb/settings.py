import os
import django_heroku
from celery.schedules import crontab
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR,'templates')
STATIC_DIR = os.path.join(BASE_DIR,'static')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG_STATUS', True)

ALLOWED_HOSTS = ['*']
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
    'django_session_timeout.middleware.SessionTimeoutMiddleware',
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS =[STATIC_DIR,]


# Sets date format for models
DATE_INPUT_FORMATS = ['%d-%m-%Y']

django_heroku.settings(locals())

COMPRESS_OFFLINE = True

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# SESSION_EXPIRE_SECONDS = 600  # 600 seconds = 10 minutes
# SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True

# BEGIN DJANGO-CRM Settings ----------------------------------------------------------------


EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'

AUTH_USER_MODEL = 'common.User'

STORAGE_TYPE = os.getenv('STORAGE_TYPE', 'normal')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATIC_URL = '/static/'
STATICFILES_DIRS = (BASE_DIR + '/static',)
COMPRESS_ROOT = BASE_DIR + '/static/'

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

# celery Tasks
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'

CELERY_BEAT_SCHEDULE = {
    "runs-campaign-for-every-thiry-minutes": {
        "task": "marketing.tasks.run_all_campaigns",
        "schedule": crontab(minute=30, hour='*')
    },
    "runs-campaign-for-every-five-minutes": {
        "task": "marketing.tasks.list_all_bounces_unsubscribes",
        "schedule": crontab(minute='*/5')
    },
    "runs-scheduled-campaigns-for-every-one-hour": {
        "task": "marketing.tasks.send_scheduled_campaigns",
        "schedule": crontab(hour='*/1')
    },
    "runs-scheduled-emails-for-accounts-every-one-minute": {
        "task": "accounts.tasks.send_scheduled_emails",
        "schedule": crontab(minute='*/1')
    }
}

MAIL_SENDER = 'GOOGLE'
INACTIVE_MAIL_SENDER = 'MANDRILL'


MGUN_API_URL = os.getenv('MGUN_API_URL', '')
MGUN_API_KEY = os.getenv('MGUN_API_KEY', '')

SG_USER = os.getenv('SG_USER', '')
SG_PWD = os.getenv('SG_PWD', '')

MANDRILL_API_KEY = os.getenv('MANDRILL_API_KEY', '')


try:
    from .dev_settings import *
except ImportError:
    pass
# For Local host http://127.0.0.1:8000/
# GP_CLIENT_ID = os.getenv('GP_CLIENT_ID', '260552032070-vfh4keifnnnou3f5v9uj7jrk4a67t257.apps.googleusercontent.com')
# GP_CLIENT_SECRET = os.getenv('GP_CLIENT_SECRET', 'qYkKQy42MOWVuITtyO14Hnd2')
# ENABLE_GOOGLE_LOGIN = os.getenv('ENABLE_GOOGLE_LOGIN', True)

GP_CLIENT_ID = os.getenv('GP_CLIENT_ID', '811390074376-nofhojo6rvkugen6u4hotpobl2rlcsg6.apps.googleusercontent.com')
GP_CLIENT_SECRET = os.getenv('GP_CLIENT_SECRET', '00IWTU5F5tbaxYZPIeioDSAA')
ENABLE_GOOGLE_LOGIN = os.getenv('ENABLE_GOOGLE_LOGIN', True)

MARKETING_REPLY_EMAIL = 'hellow@projectembrace.com'

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

# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://127.0.0.1:6379",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         }
#     }
# }

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'proememails@gmail.com'
EMAIL_HOST_PASSWORD = 'meohvgatpjcdrnyt'

PASSWORD_RESET_MAIL_FROM_USER = os.getenv('PASSWORD_RESET_MAIL_FROM_USER', 'proememails@gmail.com')

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
#             'filename': 'debugging.log',
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
