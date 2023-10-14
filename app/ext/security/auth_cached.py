# -*- coding: utf-8 -*-

from functools import wraps
from app.config.local_settings import HEADER_API_KEY, TOKEN_TYPE, SESSION_EXPIRE_TIME, STDR_UTC_HOUR
from flask import request
from datetime import datetime, timedelta
from app.ext.rest import Rest, HttpStatus
# from app.ext.sessions import get_current_session, terminate_session
from .crypto import generate_salt
from .auth_status import AuthStatus
from .auth_profiles import AuthProfiles
import logging as log
from app import app
from app import cache
from flask import jsonify


class Auth(object):
    """
    Main class for decorate wrappers
    """

    NAME_AUTH_ROLE = 'name_user_role'
    SESSION_NAME = 'auth_session'
    AUTH_SESSION_NAME = 'authorization'
    ACCESS_TOKEN = 'access_token'
    BEARER_TOKEN_LENGTH = 37
    ACCESS_TOKEN_LENGTH = 30

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

    # check
    @classmethod
    def get_access_token(self, apikey):
        #print("get_access_token fn", apikey)
        if apikey is None or not apikey:
            log.warning("Auth get_access_token the api key was not provided")
            return 709, AuthStatus.INVALID_HEADERS
        elif len(apikey) == self.BEARER_TOKEN_LENGTH:
            # get the token type
            token_type = apikey[:6]

            if TOKEN_TYPE == token_type:
                key_token = apikey[-30:]
                #print("el key_token:", key_token, "le len", len(key_token))
                if len(key_token) == self.ACCESS_TOKEN_LENGTH:
                    # get the raw token
                    return None, key_token
                else:
                    return 711, AuthStatus.INVALID_API_KEY_LENGTH
            else:
                return 710, AuthStatus.INVALID_TOKEN_TYPE
        else:
            return 711, AuthStatus.INVALID_API_KEY_LENGTH

        return 712, AuthStatus.UNEXPECTED_ERROR

    # check
    @classmethod
    def get_current_session(self, key=None):
        #print("get_current_session fn", key)
        if key is None:
            return None
            # key = self.get_access_token()
            # key = self.get_header_api_key()

        try:
            user_session = cache.get(key)
            if user_session:
                #print("get_current_session...", user_session)
                return user_session
        except Exception as e:
            print("Auth get_current_session Exception:", e)

        return None

    # check
    @classmethod
    def validate_session(self, apikey):
        #print("Auth validate_session fn:", apikey)
        if apikey is None or not apikey:
            log.warning("Auth validate_session the api key was not provided")
            return 709, AuthStatus.MISSING_AUTH_KEY

        session_token = None
        current_session = self.get_current_session(apikey)
        #print("get_current_session current_session:", current_session)

        if current_session is not None:
            if self.ACCESS_TOKEN in current_session:
                session_token = current_session[self.ACCESS_TOKEN]
                print("ACCESS_TOKEN in the current_session:", session_token)
            else:
                return 714, AuthStatus.MISSING_AUTH_KEY

            if apikey == session_token:
                #print("apikey == session_token:")
                # check expired session
                return None, None
            else:
                return 715, AuthStatus.INVALID_API_KEY
        else:
            return 716, AuthStatus.SESSION_NOT_EXISTS

        return 712, AuthStatus.UNEXPECTED_ERROR

    # check
    @classmethod
    def remove_session(self, key=None):
        print("remove_session fn", key)

        try:
            if key is None:
                # cache.flush_all()
                cache.clear()
                return None

            cache.delete(key)
        except Exception as e:
            print("Auth remove_session Exception:", e)

        return None

    # ready
    @classmethod
    def create_session(self, key=None, data=None):
        try:
            cached = cache.get(key)
            if cached:
                #print("create_session is caching...", cached)
                return

            cache.set(key, data, timeout=SESSION_EXPIRE_TIME)
        except Exception as e:
            print("Auth create_session Exception:", e)

    @classmethod
    def get_from_session(self, key, value=None):
        if key is None:
            return None

        if value is None:
            return None

        try:
            user_session = cache.get(key)
            if user_session:
                #print("get_from_session...", user_session)
                if value in user_session:
                    return user_session[value]
            return None
        except Exception as e:
            print("Auth get_from_session Exception:", e)
        return None

    # Check
    @classmethod
    def has_role_of(self, *expected_args):
        def validate_role(func):
            @wraps(func)
            def wrapper(*args, **kwargs):

                error_code, header_api_key = self.get_header_api_key()
                if error_code is not None:
                    print("Auth validate_role get_header_api_key error:", error_code, "message:", header_api_key)
                    return Rest.response(401, HttpStatus.UNAUTHORIZED, errors=header_api_key, status_code=error_code)

                error_code, access_token = self.get_access_token(header_api_key)

                if error_code is not None:
                    print("Auth validate_role get_access_token error:", error_code, "message:", access_token)
                    return Rest.response(401, HttpStatus.UNAUTHORIZED, errors=access_token, status_code=error_code)

                name_user_role = None
                name_user_role = self.get_from_session(access_token, self.NAME_AUTH_ROLE)
                #print("name_user_role ********:", name_user_role)
                if name_user_role is None:
                    return Rest.response(401, HttpStatus.UNAUTHORIZED, errors=AuthStatus.MISSING_ROLE, status_code=717)

                try:
                    # name_user_role
                    # GUEST (el que tien el usuario logueado)

                    # AuthProfiles.ROLES
                    # ['GOTU', 'ADMIN', 'SHOPKEEPERS', 'CUSTOMERS', 'REGULAR_USER', 'GUEST']
                    # (los roles de la DB)

                    # expected_args
                    # GOTU, ADMIN (el que puede hacer)
                    allowed_roles = AuthProfiles.ROLES
                    #print("try allowed_roles:", allowed_roles)
                    #print("try expected_args:", expected_args, "type:", type(expected_args))
                    #print("try current user role:", name_user_role)

                    if allowed_roles is not None:
                        if name_user_role in allowed_roles:
                            #print ("allowed_roles -****************", allowed_roles)
                            if name_user_role in expected_args:
                                pass
                            else:
                                return Rest.response(401, HttpStatus.UNAUTHORIZED, errors=AuthStatus.INVALID_ROLE, status_code=718)
                        else:
                            return Rest.response(401, HttpStatus.UNAUTHORIZED, errors=AuthStatus.MISSING_ROLE, status_code=719)
                    else:
                        return Rest.response(401, HttpStatus.UNAUTHORIZED, errors=AuthStatus.MISSING_PRIMITIVE_ROLE, status_code=720)

                except Exception as e:
                    print("Auth validate_role Exception:", e)
                    return Rest.response(400, AuthStatus.UNEXPECTED_ERROR, errors=str(e))

                return func(*args, **kwargs)
            return wrapper
        return validate_role

    # Check
    @classmethod
    def obtain_key_token(self, *expected_args):
        def validating(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                print("obtain_key_token:", expected_args)
                try:
                    import inspect
                    error_code, header_api_key = self.get_header_api_key()

                    if error_code is None:

                        error_code, api_access_token = self.get_access_token(header_api_key)
                        if error_code is None:
                            if 'token' in inspect.getargspec(func).args:
                                kwargs['token'] = api_access_token

                except Exception as e:
                    print("Auth clear_session Exception:", e)
                return func(*args, **kwargs)
            return wrapper
        return validating

    # check
    @classmethod
    def get_header_api_key(self):
        try:
            # return request.headers.get(HEADER_API_KEY)
            header_api_key = request.headers.get(HEADER_API_KEY)
            if header_api_key is None or not header_api_key:
                print("Auth get_header_api_key AuthStatus.INVALID_HEADERS")
                return 709, AuthStatus.INVALID_HEADERS
            return None, header_api_key
        except Exception as e:
            print("Auth get_header_api_key Exception:", e)

        return 712, AuthStatus.UNEXPECTED_ERROR

    # check
    @classmethod
    def require_auth_session(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            error_code, header_api_key = self.get_header_api_key()

            if error_code is not None:
                print("Auth require_auth_session get_header_api_key error:", error_code, "message:", header_api_key)
                return Rest.response(401, HttpStatus.UNAUTHORIZED, errors=header_api_key, status_code=error_code)

            error_code, api_access_token = self.get_access_token(header_api_key)

            if error_code is not None:
                print("Auth require_auth_session get_access_token error:", error_code, "message:", api_access_token)
                return Rest.response(401, HttpStatus.UNAUTHORIZED, errors=api_access_token, status_code=error_code)

            error_code, message_code = self.validate_session(api_access_token)

            if error_code is not None:
                print("Auth require_auth_session validate_token_header error:", error_code, "message:", message_code)
                return Rest.response(401, HttpStatus.UNAUTHORIZED, errors=message_code, status_code=error_code)

            return func(*args, **kwargs)
        return wrapper

    # check
    @classmethod
    def info_session(self):
        error_code, header_api_key = self.get_header_api_key()

        if error_code is not None:
            print("Auth require_auth_session get_header_api_key error:", error_code, "message:", header_api_key)
            return Rest.response(401, HttpStatus.UNAUTHORIZED, errors=header_api_key, status_code=error_code)

        error_code, api_access_token = self.get_access_token(header_api_key)

        if error_code is not None:
            print("Auth require_auth_session get_access_token error:", error_code, "message:", api_access_token)
            return Rest.response(401, HttpStatus.UNAUTHORIZED, errors=api_access_token, status_code=error_code)
        print('api_access_token++', api_access_token)
        result = self.get_current_session(api_access_token)

        return result