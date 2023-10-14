from flask import request
from app.ext.security import Auth
from app.ext.security.auth_cached import Auth as auth
from app.ext.security.crypto import generate_salt
from app.ext.rest import Rest, HttpStatus
from app.ext.resource_handler import ResourceHandler
from app.config.local_settings import TOKEN_TYPE
from app.oauth_clients.models.OauthClients import OauthClients
from app.users.models.Users import Users
from app.roles.models.Roles import Roles
from app.mobiles.models.Mobiles import Mobiles
from app.commerce.models.Commerces import Commerces
import hashlib


class ViewLogin(ResourceHandler):

    def get(self):
        return Rest.response(401, HttpStatus.UNAUTHORIZED)

    @Auth.validate_request("username", "password", "client_secret")
    def post(self):
        content = request.get_json()
        username = content.get('username', None)
        password = content.get('password', None)
        client_secret = content.get('client_secret', None)

        # cached = cache.get(uuid)
        cached = auth.get_current_session(username)
        print("checkin cache...", cached)
        if cached:
            print("login is caching...", cached)
            return Rest.response(200, HttpStatus.OK, cached)

        oauth_client_to_find = OauthClients.get_by_id(client_secret)
        if oauth_client_to_find is None:
            return Rest.response(400, HttpStatus.UNAUTHORIZED, {'message': 'Unauthorized client_secret'})

        try:
            resp = Users.get_by('username',username)
            #validar contraseña
            if resp is not None:
                if resp[0]['origin'] == 'WEB':
                    if resp[0]['password'] == hashlib.sha256(str(password).encode('utf-8')).hexdigest():
                        if len(resp) > 0:
                            token = generate_salt()

                            resp[0]['token_type'] = TOKEN_TYPE
                            resp[0]['access_token'] = token

                            auth.create_session(token, resp[0])
                            roles = Roles.get_by('name', resp[0]['name_user_role'])
                            json = {
                                "access_token": token,
                                "created_at": resp[0]['created_at'],
                                "key": resp[0]['key'],
                                "name_user_role": resp[0]['name_user_role'],
                                "role_id": resp[0]['role_id'],
                                "token_type": TOKEN_TYPE,
                                "username": resp[0]['username'],
                                "permissions": roles[0]['permissions']
                            }

                            return Rest.response(200, HttpStatus.OK, json)
                        else:
                            return Rest.response(400, HttpStatus.RESOURCE_NOT_EXIST, resp)
                    else:
                        return Rest.response(400, "Wrong passwordt", []) 
                else:       
                    return Rest.response(400, "User incorret", [])                
            else:
                return Rest.response(400, "User does not exist", [])
        except Exception as e:
            print("LoginView POST Exception:", e)
            return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, {'reason': str(e)})

    def put(self, id=0):
        return Rest.response(401, HttpStatus.UNAUTHORIZED)

    def delete(self, id=0):
        return Rest.response(401, HttpStatus.UNAUTHORIZED)


class ViewLoginMovil(ResourceHandler):

    def get(self):
        return Rest.response(401, HttpStatus.UNAUTHORIZED)

    @Auth.validate_request("username", "password", "mac", "commerce", "client_secret")
    def post(self):
        content = request.get_json()
        username = content.get('username', None)
        password = content.get('password', None)
        mac = content.get('mac', None)
        commerce = content.get('commerce', None)
        client_secret = content.get('client_secret', None)

        # cached = cache.get(uuid)
        cached = auth.get_current_session(username)
        print("checkin cache...", cached)
        if cached:
            print("login is caching...", cached)
            return Rest.response(200, HttpStatus.OK, cached)

        oauth_client_to_find = OauthClients.get_by_id(client_secret)
        if oauth_client_to_find is None:
            return Rest.response(400, HttpStatus.UNAUTHORIZED, {'message': 'Unauthorized client_secret'})

        try:
            resp = Users.get_by('username',username)
            #validar contraseña
            if resp is not None:
                if resp[0]['origin'] == 'MOVIL':
                    if resp[0]['password'] == hashlib.sha256(str(password).encode('utf-8')).hexdigest():
                        info_commerces = Commerces.get_by('code', str(commerce))
                        if info_commerces is not None:   
                            mobil = Mobiles.get_by('mac', str(mac))                        
                            if mobil is not None:
                                if len(resp) > 0:
                                    list_mobiles =info_commerces[0]['mobiles']
                                    if list_mobiles.count(str(mobil[0]['key'])) == 0:
                                        return Rest.response(400, HttpStatus.RESOURCE_NOT_EXIST, {'rason':'Mobil no registrado con el comercio'})
                                    token = generate_salt()

                                    resp[0]['token_type'] = TOKEN_TYPE
                                    resp[0]['access_token'] = token
                                    resp[0]['code_commerce'] = info_commerces[0]['code']
                                    resp[0]['mac_mobil'] = str(mobil[0]['key'])
                                    auth.create_session(token, resp[0])
                                    roles = Roles.get_by('name', resp[0]['name_user_role'])
                                    json = {
                                        "access_token": token,
                                        "created_at": resp[0]['created_at'],
                                        "key": resp[0]['key'],
                                        "name_user_role": resp[0]['name_user_role'],
                                        "role_id": resp[0]['role_id'],
                                        "token_type": TOKEN_TYPE,
                                        "username": resp[0]['username'],
                                        "permissions": roles[0]['permissions']
                                    }

                                    return Rest.response(200, HttpStatus.OK, json)
                                else:
                                    return Rest.response(400, HttpStatus.RESOURCE_NOT_EXIST, resp)
                            else:
                                return Rest.response(400, HttpStatus.RESOURCE_NOT_EXIST, {'rason':'Unregistered mobile'})        
                        else:
                            return Rest.response(400, HttpStatus.RESOURCE_NOT_EXIST, {'rason':'Unregistered trade'}) 
                    else:
                        return Rest.response(400, "Wrong passwordt", []) 
                else:       
                    return Rest.response(400, "User incorret", [])            
            else:
                return Rest.response(400, "User does not exist", [])
        except Exception as e:
            print("LoginView POST Exception:", e)
            return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, {'reason': str(e)})

    def put(self, id=0):
        return Rest.response(401, HttpStatus.UNAUTHORIZED)

    def delete(self, id=0):
        return Rest.response(401, HttpStatus.UNAUTHORIZED)
