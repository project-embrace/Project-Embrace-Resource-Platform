import os
# Make this unique, and don't share it with anybody.
# http://www.miniwebtool.com/django-secret-key-generator/
SECRET_KEY = '&5=4*=-bdbv%m!942+)pz2_t#$*zh%58rbdhe4=5tbtu-n!g0n'


# Email Server Settings
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = os.getenv('GMAIL_USER', 'proememails@gmail.com')
EMAIL_HOST_PASSWORD = os.getenv('GMAIL_PASS', 'bgxgjxtsxryrtavl')
EMAIL_PORT = 465
EMAIL_USE_TLS = True


# Database Settings
# postgresql-cylindrical-45992 'HEROKU_POSTGRESQL_BLACK'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'd7jibjvnj3lli7',
        'USER': 'cbxohzajxojsss',
        'PASSWORD':'dc7c4fcee7cc8e347b36015922e651c4b058d1525d939b8afc914c3b765f6659',
        'HOST': 'ec2-107-20-173-2.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}

# Server Customizations
ADMIN_EMAIL = "projectembracedata@gmail.com"
URL_FOR_LINKS = "https://www.projectembrace.org"


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'US/Eastern'
USE_I18N = True
USE_L10N = True
USE_TZ = True
