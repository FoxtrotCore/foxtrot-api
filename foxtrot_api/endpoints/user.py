from flask_restful import Resource


class UserEndpoint(Resource):
    """
    `/user/<username>` endpoint
    """

    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')

    def get(self, username: str) -> dict:
        return {'message': username}
