"""
Django settings for fapva project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"),]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-grl+!8ln7@_0he-dyd3e9!^5=!)9*mrc3ufs!_)q2kev*@rzgj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition


DJANGO_APPS = (
    "daphne",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django.contrib.sites"
)

THIRD_PARTY_APPS = (
    'rest_framework',
    'rest_framework.authtoken',
    'storages',
    "django.contrib.postgres",
    "debug_toolbar",
    'oauth2_provider',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook'
)


PROJECT_APPS = (
    "main",
    "fapva",
    "api",
    "web",
    "web.administrator",
    "api.users",
    "api.services",
    "api.order"
)

DEBUG_APPS = (
    'corsheaders',
)

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS + DEBUG_APPS



# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels.layers.RedisChannelLayer',
#         'CONFIG': {
#             'hosts': [('localhost', 6379)],
#         },
#     },
# }

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
        'CONFIG': {
            # 'hosts': [('127.0.0.1', 6379)],
        }
    }
}


MIDDLEWARE = [
    # 'corsheaders.middleware.CorsMiddleware',
    # 'django.middleware.security.SecurityMiddleware',
    # 'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.middleware.locale.LocaleMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request'
)

ROOT_URLCONF = 'fapva.urls'


DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

INTERNAL_IPS = [
    '192.168.18.177',
    '127.0.0.1',
    '0.0.0.0',
    'localhost',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'fapva.context_processors.wallet_detail'
            ],
        },
    },
]

# WSGI_APPLICATION = 'fapva.wsgi.application'
ASGI_APPLICATION = 'fapva.asgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'fapva',
        'USER': os.getenv('PG_USER', 'postgres'),
        'PASSWORD': os.getenv('PG_PASSWD', 'admin'),
        'HOST': os.getenv('PG_HOST', 'localhost'),
        'PORT': '5432',
    }

}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

LOGIN_URL = '/admin/login/'

REST_FRAMEWORK = {
    # "EXCEPTION_HANDLER": "api.permissions.custom_exception_handler",
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}
CORS_ORIGIN_ALLOW_ALL = True
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.AllowAllUsersModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'oauth2_provider.backends.OAuth2Backend',
]

HOST_URL = os.getenv('HOST_URL', 'http://127.0.0.1:8012')
AUTHORIZATION_SERVER_URL = f'{HOST_URL}/api/oauth/token/'
REVOKE_TOKEN_URL = os.getenv(
    'REVOKE_TOKEN_URLs', f'{HOST_URL}/api/oauth/revoke-token/'
)

SENDGRID_API_KEY = ""

OAUTH_CLIENT_ID = 'PYjR5Lnidge4lYl2YRGtqaKkJwdf9DX5KNBbvjOO'  # os.getenv('OAUTH_CLIENT_ID', 'gZUXTS8pj4Wu2pBvd3Z8XBd0rJVUOLfbeHHQe7Tx')

OAUTH_CLIENT_SECRET = '7VCVPN6GHZOY1VCswyEK0kX1tzPbHKH14vtxjRyrHysQphEfu8knASWJ0VDCr2g37qkZf659EFWzzmYVgGfz8ZHc7bMKIwWiOkbXSupbt2VjbdkfOstmHnhRVRcve8SW'


SUPER_ADMIN = ["superadmin@yopmail.com"]


# SOCIAL_AUTH_FACEBOOK_KEY = '1423669784773134'
# SOCIAL_AUTH_FACEBOOK_SECRET = '7660c2ab9af04cd027b00b8b8d0a2fb6'
# FACEBOOK_GRAPH_URL = "https://graph.facebook.com/"
# SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = "825968193665-3unck54smcqs2nmv14qkmg1fu71h61v9.apps.googleusercontent.com"
# SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "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"
# # Define SOCIAL_AUTH_FACEBOOK_SCOPE to get extra permissions from Facebook.
# # Email is not sent by default, to get it, you must request the email permission.
# SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
# SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
#     'fields': 'id, name, email'
# }
# SOCIAL_AUTH_USER_FIELDS = ["email", "username", "first_name", "password"]
#
# SOCIAL_AUTHORIZATION_SERVER_URL = f'{HOST_URL}/api/auth/convert-token'
#
# GOOGLE_BASE_URL = "https://people.googleapis.com/v1/people/me"


SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

SITE_ID = 2

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

SOCIALACCOUNT_LOGIN_ON_GET=True

PAYPAL_TEST = True


PAYPAL_CLIENT_ID = "ASkPAVjKKh5SkaEzHe2ZMv-FOByTQHVqvM5c6eq4cXrNfVo-Bc7YuSjAO4ktUd_Ok-059fLND-CssBe2"

PAYPAL_SECRET_ID = "EEI3eWDTfwJOFj0ucggMNIrAgeG9po55CziUhowrfogSWEjIoZC8ZBmtvR0OOFfG9x4OBw7z2U_VoPMp"

PAYPAL_URL = "https://api.sandbox.paypal.com/"

SECURE_CROSS_ORIGIN_OPENER_POLICY='same-origin-allow-popups'