import logging
from . import app, APP_NAME, LOG_DIR, LOG_FORMAT

LOG_HANDLERS = [
    (logging.INFO, logging.FileHandler(filename=f'{LOG_DIR}/info.log')),
    (logging.WARN, logging.FileHandler(filename=f'{LOG_DIR}/warn.log')),
    (logging.DEBUG, logging.FileHandler(filename=f'{LOG_DIR}/debug.log')),
    (logging.ERROR, logging.FileHandler(filename=f'{LOG_DIR}/error.log')),
]


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
