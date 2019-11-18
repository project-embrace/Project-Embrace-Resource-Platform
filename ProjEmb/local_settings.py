import os
# Make this unique, and don't share it with anybody.
# http://www.miniwebtool.com/django-secret-key-generator/
SECRET_KEY = '&5=4*=-bdbv%m!942+)pz2_t#$*zh%58rbdhe4=5tbtu-n!g0n'


# Email Server Settings
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = os.getenv('proememails@gmail.com', '')
EMAIL_HOST_PASSWORD = os.getenv('meohvgatpjcdrnyt', '')
EMAIL_PORT = 465
EMAIL_USE_TLS = True


# Database Settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'd1nvalp9fu04ti',
        'USER': 'sawdzaccadzqbi',
        'PASSWORD':'2bf198630fad777e0aad364fd5dbf1a60ea63628fbe263c5e8254c340d282352',
        'HOST': 'ec2-107-21-226-44.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}

# Server Customizations
ADMIN_EMAIL = "projectembracedata@gmail.com"
URL_FOR_LINKS = "https://www.projectembrace.org"


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Denver'
USE_I18N = True
USE_L10N = True
USE_TZ = True
