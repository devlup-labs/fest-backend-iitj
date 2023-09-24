import os
from pathlib import Path
from datetime import timedelta
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', cast=str)

DEBUG = config('DEBUG', default=False, cast=bool)
DEVELOPMENT = config('DEVELOPMENT', default=False, cast=bool)

ALLOWED_HOSTS = ['*']
BASE_FRONTEND_URL = config('BASE_FRONTEND_URL', default="http://localhost:3000")
BASE_BACKEND_URL = config('BASE_BACKEND_URL', default="http://localhost:8000")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'import_export',
    'accounts',
    'events',
    'coreteam',
    'sponsors',
    'ckeditor',
    'ckeditor_uploader',
    'corsheaders',
    'debug_toolbar',
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

APP_SECRET = config('APP_SECRET')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'frontend')],
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

WSGI_APPLICATION = 'backend.wsgi.application'

INTERNAL_IPS = [
    "127.0.0.1",
]

if DEVELOPMENT:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config("POSTGRES_DB_NAME"),
            'USER': config("POSTGRES_DB_USER"),
            'PASSWORD': config("POSTGRES_DB_PASSWORD"),
            'HOST': config("POSTGRES_DB_HOST", default="localhost"),
            'PORT': config("POSTGRES_DB_PORT", default=5432, cast=int),
        },
        'sponsors': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        },
    }

    DATABASE_ROUTERS = [
        'backend.dbRouters.SQLiteRouter',
    ]

AUTH_USER_MODEL = 'accounts.User'

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

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

DEFAULT_FROM_EMAIL = '"Festival, IIT Jodhpur" <no-reply@festival@iitj.co.in>'
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = config("EMAIL_PORT")
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_ROOT = os.path.join(BASE_DIR, config('STATIC_PATH', default='staticfiles', cast=str))  # type: ignore
STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DEFAULT_PROFILE_IMAGE_URL = config("DEFAULT_PROFILE_IMAGE_URL")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'registration.authenticate.CustomAuthentication',
    ],
}

# Simple JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=15),
    'ROTATE_REFRESH_TOKENS': False,
}

# CKEditor
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_RESTRICT_BY_USER = True
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Basic',
        'width': '100%',
        'tabSpaces': 4,
        'mathJaxLib': 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-AMS_HTML',
        'toolbar_Basic': [
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            # {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'formulae', 'items': ['Mathjax']},
            {'name': 'insert',
             'items': ['Image', 'Table', 'HorizontalRule', 'Smiley', ]},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', ]},
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
        ],
        'extraPlugins': ','.join([
            'uploadimage',
            'div',
            'autolink',
            'iframe',
            'embed',
            'embedsemantic',
            'autoembed',
            'autogrow',
            'uploadimage',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'mathjax',
            'codesnippet',
        ]),
    },
}


# Google OAuth2 settings
GOOGLE_OAUTH2_CLIENT_ID = config('DJANGO_GOOGLE_OAUTH2_CLIENT_ID', cast=str)
GOOGLE_OAUTH2_CLIENT_SECRET = config('DJANGO_GOOGLE_OAUTH2_CLIENT_SECRET', cast=str)
