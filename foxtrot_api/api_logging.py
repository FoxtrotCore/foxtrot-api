import logging
import flask
from foxtrot_api import LOG_DIR, LOG_FORMAT

LOG_HANDLERS = [
    (logging.INFO, logging.FileHandler(filename=f'{LOG_DIR}/info.log')),
    (logging.WARN, logging.FileHandler(filename=f'{LOG_DIR}/warn.log')),
    (logging.DEBUG, logging.FileHandler(filename=f'{LOG_DIR}/debug.log')),
    (logging.ERROR, logging.FileHandler(filename=f'{LOG_DIR}/error.log')),
]


def init_logging(log_name: str, app: flask.Flask) -> flask.Flask:
    for level, handler in LOG_HANDLERS:
        handler.setLevel(level)
        handler.setFormatter(LOG_FORMAT)
        app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    return app
