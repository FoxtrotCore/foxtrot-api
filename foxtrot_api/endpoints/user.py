from flask_restful import Resource


class UserEndpoint(Resource):
    """
    `/user/<username>` endpoint
    """

    def get(self, username: str) -> dict:
        return {'message': username}
