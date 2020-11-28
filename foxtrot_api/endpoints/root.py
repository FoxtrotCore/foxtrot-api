import foxtrot_api as fa
from flask_restful import Resource


class RootEndpoint(Resource):
    """
    `/` endpoint
    """

    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')

    def get(self) -> str:
        self.logger.info('Got request for /')
        return {'message': f'Foxtrot API v{fa.APP_VERSION}. See {fa.APP_URL}'
                           ' for documentation and usage.'}
