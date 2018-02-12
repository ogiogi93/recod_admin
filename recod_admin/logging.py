import logging
from django.conf import settings


def getLogger(name):
    return logging.getLogger('%s.%s' % (settings.LOGGING_PREFIX, name))
