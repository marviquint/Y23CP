"""
Django settings for Y23CP project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'App_Secret_Key'

#SECRET_KEY = 'App_Secret_Key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SMTP email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email_address'  # your email address
EMAIL_HOST_PASSWORD = 'your_email_password'  # your email password


# EMAIL_HOST_USER = 'your_email_address'  # your email address
# EMAIL_HOST_PASSWORD = 'your_email_password'  # your email password

# default email settings
DEFAULT_FROM_EMAIL = 'your_email_address'  # your email address

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'sapphire.apps.SapphireConfig',
]

AUTH_USER_MODEL = 'sapphire.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'sapphire.views.DjangoScrapyMiddleware',
]

ROOT_URLCONF = 'Y23CP.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates'
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

WSGI_APPLICATION = 'Y23CP.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'innodata_db',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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



AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend',]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
# settings.py

# ... other settings ...

BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static',]

DATA_DIR = BASE_DIR / 'data'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ROBOTSTXT_OBEY = False

FEED_FORMAT = 'json'
FEED_URI = 'results.json'

# Define the downloads folder path
DOWNLOADS_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads", "District of Columbia Courts")


SPIDER_MIDDLEWARES = {
    'myproject.middlewares.StartSpiderMiddleware': 543,
}

SCRAPY_SETTINGS_MODULE = 'Y23CP.settings'

# Scrapy settings
SCRAPER_SETTINGS = {
    'BOT_NAME': 'scrapy_project',
    'SPIDER_MODULES': ['scrapy_project.spiders'],
    'NEWSPIDER_MODULE': 'scrapy_project.spiders',
    'ROBOTSTXT_OBEY': True,
}

# Set the path to your Scrapy project
SCRAPER_PROJECT_PATH = '/scrapy_project/scrapyproject/scrapyproject'

# Add the Scrapy project to the Python path
import sys
sys.path.append(SCRAPER_PROJECT_PATH)
