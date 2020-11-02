import foxtrot_api as f
from flask_restful import Resource


class RootEndpoint(Resource):
    """
    `/` endpoint
    """

    def get(self) -> str:
        return {'message': 'Foxtrot API. See {} for documentation and usage.'
                           .format(f.APP_DOCS)}
