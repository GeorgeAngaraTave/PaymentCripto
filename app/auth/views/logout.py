from app.ext.security import Auth
from app.ext.rest import Rest, HttpStatus
from app.ext.resource_handler import ResourceHandler


class ViewLogout(ResourceHandler):
    def get(self, token=None):
        token = Auth.get_auth_token()
        # print("logout GET obtain_key_token:", token)
        if token is not None:
            Auth.remove_session(token)
        return Rest.response(200, HttpStatus.OK)

    def post(self, token=None):
        token = Auth.get_auth_token()
        # print("logout POST obtain_key_token:", token)
        if token is not None:
            Auth.remove_session(token)
        return Rest.response(200, HttpStatus.OK)

    def put(self):
        return Rest.response(401, HttpStatus.UNAUTHORIZED)

    def delete(self):
        return Rest.response(401, HttpStatus.UNAUTHORIZED)
