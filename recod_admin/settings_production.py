from .settings import *

ENV = 'production'
DEBUG = False

STATIC_ROOT = '/var/www/recod_admin/staticfiles/'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = 'recod_admin.storage_backends.MediaStorage'
