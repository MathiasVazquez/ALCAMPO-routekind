from .base import *  # NOQA
from .base import env
from decouple import config
import dj_database_url
import os
# Base
DEBUG = True

# Security
SECRET_KEY = config('DJANGO_SECRET_KEY', default='PB3aGvTmCkzaLGRAxDc3aMayKTPTDd5usT8gw4pCmKOk5AlJjh12pTrnNgQyOHCH')
ALLOWED_HOSTS = [
    "localhost",
    "0.0.0.0",
    "127.0.0.1",
    #'routekind-back-e537177bedf1.herokuapp.com',
    'routekind-back.probusinesspy.xyz'
]

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL')
    )
}

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

# Templates
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG  # NOQA

# Email
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025

# django-extensions
INSTALLED_APPS += ['django_extensions']  # noqa F405

# Celery
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True


# Security
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = env.bool('DJANGO_SECURE_SSL_REDIRECT', default=True)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool('DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True)
SECURE_HSTS_PRELOAD = env.bool('DJANGO_SECURE_HSTS_PRELOAD', default=True)
SECURE_CONTENT_TYPE_NOSNIFF = env.bool('DJANGO_SECURE_CONTENT_TYPE_NOSNIFF', default=True)

# """Production settings."""

# from .base import *  # NOQA
# from .base import env

# # Base
# SECRET_KEY = env('DJANGO_SECRET_KEY')
# ALLOWED_HOSTS = [
#     "localhost",
#     "0.0.0.0",
#     "127.0.0.1",
#     'routekind-back-e537177bedf1.herokuapp.com'
# ]

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / "db.sqlite3",
#     }
# }

# # DATABASES
# # DATABASES = {
# #     'default': env.db('DATABASE_URL'),
# # }
# # DATABASES = {
# #     'default': {
# #         'ENGINE': 'django.db.backends.postgresql',
# #         'NAME': os.environ.get(POSTGRES_DB),
# #         'USER': os.environ.get(POSTGRES_USER),
# #         'PASSWORD': os.environ.get(POSTGRES_PASSWORD),
# #         'HOST': os.environ.get(POSTGRES_HOST),
# #         'PORT': os.environ.get(POSTGRES_PORT),
# #     }
# # }
# DATABASES['default']['ATOMIC_REQUESTS'] = True
# # Databases
# # DATABASES['default'] = env.db('DATABASE_URL')  # NOQA
# DATABASES['default']['ATOMIC_REQUESTS'] = True  # NOQA
# DATABASES['default']['CONN_MAX_AGE'] = env.int('CONN_MAX_AGE', default=60)  # NOQA

# # Cache
# # CACHES = {
# #     'default': {
# #         'BACKEND': 'django_redis.cache.RedisCache',
# #         'LOCATION': env('REDIS_URL'),
# #         'OPTIONS': {
# #             'CLIENT_CLASS': 'django_redis.client.DefaultClient',
# #             'IGNORE_EXCEPTIONS': True,
# #         }
# #     }
# # }

# # Security
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT = env.bool('DJANGO_SECURE_SSL_REDIRECT', default=True)
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_HSTS_SECONDS = 60
# SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool('DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True)
# SECURE_HSTS_PRELOAD = env.bool('DJANGO_SECURE_HSTS_PRELOAD', default=True)
# SECURE_CONTENT_TYPE_NOSNIFF = env.bool('DJANGO_SECURE_CONTENT_TYPE_NOSNIFF', default=True)

# '''# Storages
# INSTALLED_APPS += ['storages']  # noqa F405
# AWS_ACCESS_KEY_ID = env('DJANGO_AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = env('DJANGO_AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = env('DJANGO_AWS_STORAGE_BUCKET_NAME')
# AWS_QUERYSTRING_AUTH = False
# _AWS_EXPIRY = 60 * 60 * 24 * 7
# AWS_S3_OBJECT_PARAMETERS = {
#     'CacheControl': f'max-age={_AWS_EXPIRY}, s-maxage={_AWS_EXPIRY}, must-revalidate',
# }'''

# # Static  files
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# # # Media
# # DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# # #MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/'

# # Templates
# TEMPLATES[0]['OPTIONS']['loaders'] = [  # noqa F405
#     (
#         'django.template.loaders.cached.Loader',
#         [
#             'django.template.loaders.filesystem.Loader',
#             'django.template.loaders.app_directories.Loader',
#         ]
#     ),
# ]

# # # Email
# # DEFAULT_FROM_EMAIL = env(
# #     'DJANGO_DEFAULT_FROM_EMAIL',
# #     default='Comparte Ride <noreply@comparteride.com>'
# # )
# # SERVER_EMAIL = env('DJANGO_SERVER_EMAIL', default=DEFAULT_FROM_EMAIL)
# # EMAIL_SUBJECT_PREFIX = env('DJANGO_EMAIL_SUBJECT_PREFIX', default='[Comparte Ride]')

# # Admin
# # ADMIN_URL = env('DJANGO_ADMIN_URL')

# # Anymail (Mailgun)
# # INSTALLED_APPS += ['anymail']  # noqa F405
# # EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'
# # ANYMAIL = {
# #     'MAILGUN_API_KEY': env('MAILGUN_API_KEY'),
# #     'MAILGUN_SENDER_DOMAIN': env('MAILGUN_DOMAIN')
# # }

# # Gunicorn
# INSTALLED_APPS += ['gunicorn']  # noqa F405

# # WhiteNoise
# MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')  # noqa F405


# # Logging
# # A sample logging configuration. The only tangible logging
# # performed by this configuration is to send an email to
# # the site admins on every HTTP 500 error when DEBUG=False.
# # See https://docs.djangoproject.com/en/dev/topics/logging for
# # more details on how to customize your logging configuration.
# # LOGGING = {
# #     'version': 1,
# #     'disable_existing_loggers': False,
# #     'filters': {
# #         'require_debug_false': {
# #             '()': 'django.utils.log.RequireDebugFalse'
# #         }
# #     },
# #     'formatters': {
# #         'verbose': {
# #             'format': '%(levelname)s %(asctime)s %(module)s '
# #                       '%(process)d %(thread)d %(message)s'
# #         },
# #     },
# #     'handlers': {
# #         'mail_admins': {
# #             'level': 'ERROR',
# #             'filters': ['require_debug_false'],
# #             'class': 'django.utils.log.AdminEmailHandler'
# #         },
# #         'console': {
# #             'level': 'DEBUG',
# #             'class': 'logging.StreamHandler',
# #             'formatter': 'verbose',
# #         },
# #     },
# #     'loggers': {
# #         'django.request': {
# #             'handlers': ['mail_admins'],
# #             'level': 'ERROR',
# #             'propagate': True
# #         },
# #         'django.security.DisallowedHost': {
# #             'level': 'ERROR',
# #             'handlers': ['console', 'mail_admins'],
# #             'propagate': True
# #         }
# #     }
# # }
