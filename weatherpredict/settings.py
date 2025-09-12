"""
Django settings for weatherpredict project.
"""

import os
from pathlib import Path

# ----------------------------
# BASE DIRECTORY
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent  # Points to your project root

# ----------------------------
# SECURITY
# ----------------------------
SECRET_KEY = 'your-secret-key-here'  # Replace with your own secret key
DEBUG = True
ALLOWED_HOSTS = []

# ----------------------------
# INSTALLED APPS
# ----------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'weatherpredict',  # your app
]

# ----------------------------
# MIDDLEWARE
# ----------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',       # ✅ must come before auth
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',    # ✅ required for admin
    'django.contrib.messages.middleware.MessageMiddleware',       # ✅ required for admin
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ----------------------------
# URL CONFIG
# ----------------------------
ROOT_URLCONF = 'weatherpredict.urls'

# ----------------------------
# TEMPLATES
# ----------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "weatherpredict" / "templates"],  # Make sure templates folder exists
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

# ----------------------------
# WSGI
# ----------------------------
WSGI_APPLICATION = 'weatherpredict.wsgi.application'

# ----------------------------
# DATABASE (SQLite example)
# ----------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ----------------------------
# PASSWORD VALIDATORS
# ----------------------------
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

# ----------------------------
# INTERNATIONALIZATION
# ----------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ----------------------------
# STATIC FILES
# ----------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",  # ✅ points to the actual folder
]
STATIC_ROOT = BASE_DIR / "staticfiles"  # for collectstatic

# ----------------------------
# DEFAULT AUTO FIELD
# ----------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
