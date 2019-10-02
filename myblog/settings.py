"""
Django settings for myblog project.

Generated by 'django-admin startproject' using Django 2.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import django_heroku
# Пути сборки внутри проекта, как это: os.path.join (base_dir, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Быстрый запуск настроек развития - непригодно для производства
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# ПРЕДУПРЕЖДЕНИЕ О БЕЗОПАСНОСТИ: хранить секретный ключ, используемый в производстве секрет!
SECRET_KEY = 'q#fb!8@ina1#l-^3@ll85gtta7w&4d%mm&jxdsz4#hhi6_sofh'

# ПРЕДУПРЕЖДЕНИЕ О БЕЗОПАСНОСТИ: не работает с отладкой включено в производстве!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'voodoo-blog-development.herokuapp.com']


# определение приложений

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',

    'django_static_jquery',
    'phonenumber_field',
    'multiselectfield',

    'blog',
    'curiosity'
]

PHONENUMBER_DB_FORMAT = 'E164'
PHONENUMBER_DEFAULT_REGION = 'RU'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

ROOT_URLCONF = 'myblog.urls'

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
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'myblog.wsgi.application'

# База данных
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'd506g6k3p5qt0u',
        'USER': 'qpwlfbfqwcyvvp',
        'PASSWORD': 'b4dc56b4d253d8823b304641489130b19936218bfb18a54a9191cb8268a625b0',
        'HOST': 'ec2-75-101-133-29.compute-1.amazonaws.com',
        'PORT': '5432',
        'CONN_MAX_AGE': 500
    }
}


# проверка пароля
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# интернационализация
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# # Дополнительные места для collectstatic для поиска статических файлов.
STATICFILES_DIRS = (
   os.path.join(BASE_DIR, 'static'),
)

# # Медиа
MEDIA_ROOT = '/home/media/'
MEDIA_URL = '/media/'


# # Обслуживание статических файлов
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# # Активация Django-heroku
django_heroku.settings(locals())