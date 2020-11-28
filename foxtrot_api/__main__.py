import flask
import flask_restful
from flask_cors import CORS
from foxtrot_api.api_logging import init_logging
from foxtrot_api.endpoints import (
    RootEndpoint,
    BareUserEndpoint,
    UserEndpoint
)

# API application build + resource endpoints
app = flask.Flask(__name__)
api = flask_restful.Api(app)

# Enable cross origin resource sharing
CORS(app)

# Init the logger then log something
app = init_logging(__name__, app)
app.logger.info('Enabled Cross Origin Resouce Sharing')

# Add various endpoint resources
api.add_resource(RootEndpoint,
                 '/',
                 resource_class_kwargs={'logger': app.logger})
api.add_resource(BareUserEndpoint,
                 '/user',
                 resource_class_kwargs={'logger': app.logger})
api.add_resource(UserEndpoint,
                 '/user/<username>',
                 resource_class_kwargs={'logger': app.logger})


def main():
    app.logger.info('Entered callable!')
    print('Entered !')
    try:
        app.logger.info('Starting the API...')
        app.run()
    except Exception as e:
        app.logger.error('------ A fatal crash happened! ------')
        app.logger.exception(f'Crash report for exception: \'{e}\'')


if __name__ == '__main__':
    main()
