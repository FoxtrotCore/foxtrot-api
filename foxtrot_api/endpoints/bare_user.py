from flask import redirect
from flask_restful import Resource


class BareUserEndpoint(Resource):
    """
    `/user` endpoint
    """

    def get(self) -> dict:
        return redirect('/', code=302)
