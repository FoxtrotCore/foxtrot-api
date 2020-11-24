from flask_restful import Resource


class RootEndpoint(Resource):
    """
    `/` endpoint
    """

    def get(self) -> str:
        return {'message': f'Foxtrot API. See for documentation and usage.'}
