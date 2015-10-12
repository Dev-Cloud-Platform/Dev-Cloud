# -*- coding: utf-8 -*-
# @COPYRIGHT_begin
#
# Copyright [2015] Michał Szczygieł, M4GiK Software
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# @COPYRIGHT_end

"""Production settings and globals."""
from os import environ

# from memcacheify import memcacheify
# from postgresify import postgresify
# from S3 import CallingFormat
from common import *

########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = environ.get('EMAIL_HOST', config.EMAIL_HOST)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-password
EMAIL_HOST_PASSWORD = environ.get('EMAIL_HOST_PASSWORD', config.EMAIL_HOST_PASSWORD)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-user
EMAIL_HOST_USER = environ.get('EMAIL_HOST_USER', config.EMAIL_HOST_USER)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = environ.get('EMAIL_PORT', config.EMAIL_PORT)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = '[%s] ' % SITE_NAME

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-use-tls
EMAIL_USE_TLS = True

EMAIL_FAIL_SILENTLY = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = EMAIL_HOST_USER
########## END EMAIL CONFIGURATION


########## DATABASE CONFIGURATION
# DATABASES = postgresify()

# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Dev_Cloud_db',
        'USER': 'root',
        'PASSWORD': 'qetuo1357',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
########## END DATABASE CONFIGURATION


########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
# CACHES = memcacheify()

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
########## END CACHE CONFIGURATION


########## CELERY CONFIGURATION
# See: http://docs.celeryproject.org/en/latest/configuration.html#broker-transport
BROKER_TRANSPORT = 'redis'

# Set this number to the amount of allowed concurrent connections on your AMQP
# provider, divided by the amount of active workers you have.
#
# For example, if you have the 'Little Lemur' CloudAMQP plan (their free tier),
# they allow 3 concurrent connections. So if you run a single worker, you'd
# want this number to be 3. If you had 3 workers running, you'd lower this
# number to 1, since 3 workers each maintaining one open connection = 3
# connections total.
#
# See: http://docs.celeryproject.org/en/latest/configuration.html#broker-pool-limit
BROKER_POOL_LIMIT = 3

# See: http://docs.celeryproject.org/en/latest/configuration.html#broker-connection-max-retries
BROKER_CONNECTION_MAX_RETRIES = 0

# See: http://docs.celeryproject.org/en/latest/configuration.html#broker-url
BROKER_URL = 'redis://' + CELERY_IP_ADDRESS + ':6379/0'

# See: http://docs.celeryproject.org/en/latest/configuration.html#celery-result-backend
CELERY_RESULT_BACKEND = 'redis://' + CELERY_IP_ADDRESS + ':6379/0'

# See: http://docs.celeryq.org/en/latest/configuration.html#celery-always-eager
CELERY_ALWAYS_EAGER = False

# See: http://docs.celeryproject.org/en/latest/configuration.html#celery-eager-propagates-exceptions
CELERY_EAGER_PROPAGATES_EXCEPTIONS = False
########## END CELERY CONFIGURATION


########## STORAGE CONFIGURATION
# See: http://django-storages.readthedocs.org/en/latest/index.html
# INSTALLED_APPS += (
#     'storages',
# )
#
# # See: http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html#settings
# STATICFILES_STORAGE = DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
#
# # See: http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html#settings
# AWS_CALLING_FORMAT = CallingFormat.SUBDOMAIN
#
# # See: http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html#settings
# AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID', '')
# AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY', '')
# AWS_STORAGE_BUCKET_NAME = environ.get('AWS_STORAGE_BUCKET_NAME', '')
# AWS_AUTO_CREATE_BUCKET = True
# AWS_QUERYSTRING_AUTH = False
#
# # AWS cache settings, don't change unless you know what you're doing:
# AWS_EXPIRY = 60 * 60 * 24 * 7
# AWS_HEADERS = {
#     'Cache-Control': 'max-age=%d, s-maxage=%d, must-revalidate' % (AWS_EXPIRY,
#         AWS_EXPIRY)
# }
#
# # See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
# STATIC_URL = 'https://s3.amazonaws.com/%s/' % AWS_STORAGE_BUCKET_NAME
########## END STORAGE CONFIGURATION


########## COMPRESSION CONFIGURATION
# See: http://django_compressor.readthedocs.org/en/latest/settings/#django.conf.settings.COMPRESS_OFFLINE
COMPRESS_OFFLINE = True

# See: http://django_compressor.readthedocs.org/en/latest/settings/#django.conf.settings.COMPRESS_STORAGE
# COMPRESS_STORAGE = DEFAULT_FILE_STORAGE

# See: http://django_compressor.readthedocs.org/en/latest/settings/#django.conf.settings.COMPRESS_CSS_FILTERS
COMPRESS_CSS_FILTERS += [
    'compressor.filters.cssmin.CSSMinFilter',
]

# See: http://django_compressor.readthedocs.org/en/latest/settings/#django.conf.settings.COMPRESS_JS_FILTERS
COMPRESS_JS_FILTERS += [
    'compressor.filters.jsmin.JSMinFilter',
]
########## END COMPRESSION CONFIGURATION


########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = environ.get('SECRET_KEY', SECRET_KEY)
########## END SECRET CONFIGURATION

########## ALLOWED HOSTS CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['.192.245.169.169', '.127.0.0.1']
########## END ALLOWED HOST CONFIGURATION



