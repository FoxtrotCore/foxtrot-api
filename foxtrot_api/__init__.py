import flask
import flask_restful
from flask_cors import CORS
from .logger import init
from .endpoints import RootEndpoint,  BareUserEndpoint, UserEndpoint

MAJOR = 2
MINOR = 0
PATCH = 0

APP_NAME = 'foxtrot-api'
APP_DESCRIPTION = 'An API for searching and downloading Code Lyoko ' \
                  'transcripts and subtitles.'
APP_VERSION = "{}.{}.{}".format(MAJOR, MINOR, PATCH)
APP_AUTHOR = "Dmitri McGuckin"
APP_EMAIL = 'hello@foxtrotfanatics.com'
APP_URL = "https://github.com/FoxtrotCore/foxtrot-api"
APP_DOCS = 'https://foxtrotapi.docs.apiary.io'
APP_LICENSE = 'MIT'

APP_HOST = '0.0.0.0'
APP_PORT = 8080

# Green Unicorn config and setup
bind = "{}:{}".format(APP_HOST, APP_PORT)
workers = 2

# Application logging initialization
init(__name__)

# API application build + resource endpoints
app = flask.Flask(__name__)
api = flask_restful.Api(app)

# Enable cross origin resource request
CORS(app)

# Add various endpoint resources
api.add_resource(RootEndpoint, '/')
api.add_resource(BareUserEndpoint, '/user')
api.add_resource(UserEndpoint, '/user/<username>')
