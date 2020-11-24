import foxtrot_api as fa
from flask_restful import Resource


class RootEndpoint(Resource):
    """
    `/` endpoint
    """

    def get(self) -> str:
        return {'message': f'Foxtrot API v{fa.APP_VERSION}. See {fa.APP_URL}'
                           ' for documentation and usage.'}
