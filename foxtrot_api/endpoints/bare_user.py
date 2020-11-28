from flask import redirect
from flask_restful import Resource


class BareUserEndpoint(Resource):
    """
    `/user` endpoint
    """

    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')

    def get(self) -> dict:
        return redirect('/', code=302)
