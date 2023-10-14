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

class ViewCrypto(ResourceHandler):
    decorators = [
        auth.require_auth_session,
    ]

    def get(self):
        return Rest.response(200, HttpStatus.OK, {'home': 'Welcome to BackEndBase, version ' + APP_VERSION})

    @auth.has_role_of("SUPER_ADMIN", "USER_OPERATIONAL")
    @Auth.validate_request("crypto_name", "amount")
    def post(self):
        content = request.get_json()
        cryptocurrency = content.get('crypto_name', None)
        currency = content.get('amount', None)
        operation = content.get('operation', None)

        try:
            token = generate_token()  
            if cryptocurrency == 'LITECOIN':
                BTC = cop_value(currency, cryptocurrency, token, operation)
                # print('TOKEN', TOKEN)
                # litecoin = 335.76
                # valor = currency / litecoin
            elif cryptocurrency == 'BITCOIN':
                BTC = cop_value(currency, cryptocurrency, token, operation)
                # dogecoin = 9,52
                # valor = currency / dogecoin                
            elif cryptocurrency == 'DOGECOIN':
                #BTC = cop_value(currency, cryptocurrency, token)
                BTC = {'data': {}}
                # bitcoin = 32304459.92
                # valor = currency / bitcoin
            else:     
                return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, {'reason': str('No exist money')})

            BTC_DATA = BTC['data']
            BTC_DATA['type'] = cryptocurrency
            return Rest.response(200, HttpStatus.OK, BTC_DATA)
            #return Rest.response(200, HttpStatus.OK, {'value': BTC_DATA[str(crypto_type[str(cryptocurrency)])+'_value'] ,'amount': "{0:.8f}".format(BTC_DATA['COP_to_'+str(crypto_type[str(cryptocurrency)])]), 'type': cryptocurrency })
        except Exception as e:
            print ("RoleView POST Exception:", e)
            return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, {'reason': str(e)})

    def put(self):
        return Rest.response(200, HttpStatus.OK, {'home': 'Welcome to BackEndBase, version ' + APP_VERSION})

    def delete(self):
        return Rest.response(200, HttpStatus.OK, {'home': 'Welcome to BackEndBase, version ' + APP_VERSION})

class ViewCryptoTransation(ResourceHandler):
    decorators = [
        auth.require_auth_session,
    ]

    def get(self):
        return Rest.response(200, HttpStatus.OK, {'home': 'Welcome to BackEndBase, version ' + APP_VERSION})

    @auth.has_role_of("SUPER_ADMIN", "USER_OPERATIONAL")
    @Auth.validate_request("adress_from", "amount")
    def post(self):
        content = request.get_json()
        data = {
            "adress_from": content.get('adress_from', None),
            "adress_to": "2MtngSTMTJdN2tucgPbuRp8UcW4YNxyzaoe",
            "amount": content.get('amount', None),
            "crypto_name": content.get('crypto_name', None)
        }

        try:
            token = generate_token()
            
            validate = get_balance(data, token)
                        
            if validate['status'] >= 400:
                return Rest.response(validate['status'], validate['data']['message'], validate['data']['data'])
            else:    
                result = crypto_transation(data, token)
                print('transaccion info', result)

                if result['status'] >= 400:
                    return Rest.response(result['status'], result['message'], [])
                else:    
                    info_session = auth.info_session()
                    
                    _new_Transaccion = Model_TransaccionCrypto()
                    _new_Transaccion.ticket = result['data']['txid']
                    _new_Transaccion.network = result['data']['network']
                    _new_Transaccion.amount_sent = result['data']['amount_sent']
                    _new_Transaccion.amount_withdrawn = result['data']['amount_withdrawn']
                    _new_Transaccion.code_commerce = info_session['code_commerce']
                    _new_Transaccion.mac_mobil = info_session['mac_mobil']
                    _new_Transaccion.key_users = info_session['key']
                    _new_Transaccion.datetime = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
                    result_save = Model_TransaccionCrypto.save(_new_Transaccion)    
                    
                    if result_save is None:
                        return Rest.response(200, HttpStatus.OK, result['data'])
                    else:
                        return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, {'reason': str(result)})     
                    #return Rest.response(200, HttpStatus.OK, result['data'])                 
            
        except Exception as e:
            print ("RoleView POST Exception:", e)
            return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, {'reason': str(e)})

    def put(self):
        return Rest.response(200, HttpStatus.OK, {'home': 'Welcome to BackEndBase, version ' + APP_VERSION})

    def delete(self):
        return Rest.response(200, HttpStatus.OK, {'home': 'Welcome to BackEndBase, version ' + APP_VERSION})