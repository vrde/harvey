"""This module contains all the settings for the application"""

from harvey import utils


PROXIES = {
    'http': 'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050'
}


# Crawler settings
REQUEST_CONCURRENCY = 20
REQUEST_TIMEOUT = 4
REQUEST_DOWNLOAD_TIMEOUT = 10
REQUEST_TTL = 3
REQUEST_USER_AGENT = 'harvey bot 0.0.1'


_LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '%(levelname)s [PID:%(process)d] %(asctime)s %(name)s: %(message)s'
        }
    },

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'filename': 'harvey.log',
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 5,
            'formatter': 'simple'
        }
    },

    'loggers': {
        'root': {
            'level': 'WARNING',
            'handlers': ['console']
        },
        'gevent_utils': {
            'level': 'DEBUG',
            'handlers': ['console']
        },
        'harvey': {
            'level': 'DEBUG',
            'handlers': ['console']
        }
    }
}

try:
    from local_settings import *
except ImportError:
    pass

if 'LOGGING' not in locals():
    LOGGING = {}

LOGGING = utils.update(_LOGGING, LOGGING)
