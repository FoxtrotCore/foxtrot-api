import os
import logging

MAJOR = 2
MINOR = 1
PATCH = 0

APP_NAME = 'foxtrot-api'
APP_VERSION = "{}.{}.{}".format(MAJOR, MINOR, PATCH)
APP_URL = "https://github.com/FoxtrotCore/foxtrot-api"
APP_AUTHOR = "Dmitri McGuckin"
APP_AUTHOR_EMAIL = 'hello@foxtrotfanatics.com'
APP_LICENSE = 'MIT'
APP_DESCRIPTION = 'An API for searching and downloading Code Lyoko ' \
                  'transcripts and subtitles.'

APP_DOCS = 'https://foxtrotapi.docs.apiary.io'

# Logging config
LOG_DIR = os.path.expanduser(f'~/.local/share/{APP_NAME}/')
LOG_FORMAT = logging.Formatter('[%(asctime)s][%(filename)s:%(lineno)d]'
                               '[%(levelname)s]: %(message)s')
os.makedirs(LOG_DIR, exist_ok=True)
