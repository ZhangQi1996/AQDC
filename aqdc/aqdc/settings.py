"""
Django settings for aqdc project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'z4opnv-aoc5!iyo#7sc#d)yb1l7$k$^7-@&i=6c8n@kxi=l_!x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '118.25.18.117']
ALLOWED_HOSTS = ['*']   # 注意在uwsgi容器中设置允许所有访问

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'ip_query',
    'aq_pred',
    'rest_framework',
    'xadmin',   # 添加
    'crispy_forms', # 添加
    'reversion',    # （可选）
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

X_FRAME_OPTIONS = 'SAMEORIGIN'  # 设置iframe访问
# X_FRAME_OPTIONS = 'ALLOW-FROM *' # 设置iframe访问

ROOT_URLCONF = 'aqdc.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'aqdc.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'aqdc',
        'USER': 'root',
        'PASSWORD': 'zq15067522063',
        'HOST': '120.24.217.229',
        'PORT': '3306',
    },
    'ip_query': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fis',
        'USER': 'root',
        'PASSWORD': 'zq15067522063',
        'HOST': '120.24.217.229',
        'PORT': '3306',
    },
}

DATABASE_ROUTERS = ['aqdc.db_router.DatabaseAppsRouter']

DATABASE_APPS_MAPPING = {
    # example:
    # 'app_name':'database_name',
    'ip_query': 'ip_query',
}
# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

# 每个app下的static文件对应于app下的static文件
STATIC_URL = '/static/'

STATIC_ROOT = '/pyProj/AQDC/static' # 将所有静态文件迁移到所在目录

# app外的公共文件
# STATICFILES_DIRS = ['/pyProj/AQDC/static/',] 

ADMINS = (('David', '358929931@qq.com'), ('David', '1424851327@qq.com'))
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = '18239961260@163.com'
EMAIL_HOST_PASSWORD = 'zq15067522063'


VERSION = 'v1/'

