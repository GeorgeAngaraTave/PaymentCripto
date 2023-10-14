from app.ext.resource_handler import ResourceHandler
from app.ext.rest import Rest, HttpStatus
from app.config.settings import APP_VERSION
from flask import request
from app.ext.security import Auth
from app.ext.security.auth_cached import Auth as auth
from app.ext.rest import Rest, HttpStatus
import datetime
from app.crypto.views.crypto_services import generate_token, cop_value, crypto_transation, get_balance
from app.crypto.models.TransaccionCrypto import TransaccionCrypto as Model_TransaccionCrypto

class ViewReportsTransation(ResourceHandler):
    decorators = [
        auth.require_auth_session,
    ]

    @auth.has_role_of("SUPER_ADMIN", "USER_OPERATIONAL")
    def get(self, id = 0):
        if id == 0:
            info_session = auth.info_session()
            #print('allowed_roles', info_session)
            if info_session['name_user_role'] == 'SUPER_ADMIN':
                result = Model_TransaccionCrypto.get_all()
                if len(result) > 0:
                    return Rest.response(200, HttpStatus.OK, result)
                else:
                    return Rest.response(400, HttpStatus.DEFAULT_ERROR_MESSAGE, {'reason': 'TransaccionCrypto are empty'})
                    ref = Model_TransaccionCrypto.get_ref()
                    result = ref.where(
                    'mac_mobil', '==', info_session['mac_mobil']
                    ).get()
                    
                    resp = Model_TransaccionCrypto.to_json(result, True)
                    
                    if resp is not None:
                        return Rest.response(200, HttpStatus.OK, resp)
                    else:  
                        return Rest.response(400, HttpStatus.DEFAULT_ERROR_MESSAGE, {'reason': 'TransaccionCrypto are empty'})
            elif info_session['name_user_role'] == 'USER_OPERATIONAL':
                ref = Model_TransaccionCrypto.get_ref()
                result = ref.where(
                'mac_mobil', '==', info_session['mac_mobil']
                ).get()
                
                resp = Model_TransaccionCrypto.to_json(result, True)
                
                if resp is not None:
                    return Rest.response(200, HttpStatus.OK, resp)
                else:  
                    return Rest.response(400, HttpStatus.DEFAULT_ERROR_MESSAGE, {'reason': 'TransaccionCrypto are empty'})
            else:
                return Rest.response(716, 'you dont have permission to access the requested resource')         
        else:
            result = Model_TransaccionCrypto.get_by_id(id)
            if result is not None:
                    return Rest.response(200, HttpStatus.OK, result)
            else:
                return Rest.response(400, HttpStatus.RESOURCE_NOT_EXIST)

    @auth.has_role_of("SUPER_ADMIN", "USER_OPERATIONAL")
    @Auth.validate_request("crypto_name", "amount")
    def post(self):
        return Rest.response(200, HttpStatus.OK, {'home': 'Welcome to BackEndBase, version ' + APP_VERSION})

    def put(self):
        return Rest.response(200, HttpStatus.OK, {'home': 'Welcome to BackEndBase, version ' + APP_VERSION})

    def delete(self):
        return Rest.response(200, HttpStatus.OK, {'home': 'Welcome to BackEndBase, version ' + APP_VERSION})
