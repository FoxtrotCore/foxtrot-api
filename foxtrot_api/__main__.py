import logging
import flask
import flask_restful
from flask_cors import CORS
from foxtrot_api.endpoints import (
    RootEndpoint,
    BareUserEndpoint,
    UserEndpoint
)
from . import APP_NAME, LOG_DIR, LOG_FORMAT

LOG_HANDLERS = [
    (logging.INFO, logging.FileHandler(filename=f'{LOG_DIR}/info.log')),
    (logging.WARN, logging.FileHandler(filename=f'{LOG_DIR}/warn.log')),
    (logging.DEBUG, logging.FileHandler(filename=f'{LOG_DIR}/debug.log')),
    (logging.ERROR, logging.FileHandler(filename=f'{LOG_DIR}/error.log')),
]

# API application build + resource endpoints
app = flask.Flask(__name__)
api = flask_restful.Api(app)

# Enable cross origin resource request
CORS(app)

# Add various endpoint resources
api.add_resource(RootEndpoint, '/')
api.add_resource(BareUserEndpoint, '/user')
api.add_resource(UserEndpoint, '/user/<username>')


def init_logging(log_name: str) -> logging.Logger:
    root = logging.getLogger(log_name)
    for level, handler in LOG_HANDLERS:
        handler.setLevel(level)
        handler.setFormatter(LOG_FORMAT)
        root.addHandler(handler)
    root.setLevel(logging.INFO)
    return root


def main():
    logger = init_logging(APP_NAME)
    logger.info('Entered callable!')
    print('Entered !')
    try:
        logger.info('Starting the API...')
        app.run()
    except Exception as e:
        logger.error('------ A fatal crash happened! ------')
        logger.exception(f'Crash report for exception: \'{e}\'')


if __name__ == '__main__':
    main()
