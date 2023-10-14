# -*- coding: utf-8 -*-

from flask import request
from functools import wraps
from .auth_status import AuthStatus
from datetime import datetime, timedelta
from app.ext.rest import Rest, HttpStatus
from app.ext.firebase.firestore_model import get_by
from app.config.local_settings import HEADER_API_KEY, TOKEN_TYPE, SESSION_EXPIRE_TIME, STDR_UTC_HOUR


class Auth(object):
    """
    Main class for decorate wrappers
    """

    SESSION_NAME = 'auth_session'
    AUTH_SESSION_NAME = 'authorization'
    ACCESS_TOKEN = 'access_token'

    @classmethod
    def get_current_time(self):
        now = datetime.utcnow() - timedelta(hours=STDR_UTC_HOUR)
        current_time = now.strftime('%Y-%m-%d %H:%M:%S')
        current_time = datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")
        return current_time

    @classmethod
    def get_expire_time(self):
        now = datetime.utcnow() - timedelta(hours=STDR_UTC_HOUR)
        expire_time = now + timedelta(seconds=SESSION_EXPIRE_TIME)
        return expire_time

    @classmethod
    def validate_request(self, *expected_args):
        def validating(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                missing = []
                try:
                    json_data = request.get_json(force=True)
                    if json_data is not None:
                        for field in expected_args:
                            if field not in json_data or json_data.get(field) is None or not json_data.get(field):
                                missing.append(field)
                        if len(missing) > 0:
                            return Rest.response(400, 'missing fields: ' + str(missing))
                except Exception as e:
                    return Rest.response(400, AuthStatus.UNEXPECTED_ERROR, errors=str(e))

                return func(*args, **kwargs)
            return wrapper
        return validating

    @classmethod
    def require_user_session(self, func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            apikey = request.headers.get(HEADER_API_KEY)

            if apikey is None or not apikey:
                return Rest.response(401, "The api key was not provided", [])

            elif len(apikey) == 27:
                token_type = apikey[:6]
                key_token = apikey[-20:]

                if TOKEN_TYPE != token_type:
                    return Rest.response(401, HttpStatus.UNAUTHORIZED, [])
            else:
                return Rest.response(401, HttpStatus.UNAUTHORIZED, [])

            collection = "Login"
            key = "uuid"
            result = get_by(collection, key, key_token)
            if len(result) <= 0:
                return Rest.response(401, HttpStatus.UNAUTHORIZED, [])
            return func(*args, **kwargs)
        return wrapper
