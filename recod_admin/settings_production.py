from .settings import *

ENV = 'production'
DEBUG = False

STATIC_ROOT = '/var/www/recod_admin/staticfiles/'
DEFAULT_FILE_STORAGE = 'recod_admin.storage_backends.MediaStorage'
