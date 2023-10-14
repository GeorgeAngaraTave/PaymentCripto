from flask import request
from app.ext.security import Auth
from app.ext.security.auth_cached import Auth as auth
from app.ext.rest import Rest, HttpStatus
from app.ext.resource_handler import ResourceHandler
from app.users.models.Users import Users as Model_users
from app.commerce.models.Commerces import Commerces as Model_commerce
from app.mobiles.models.Mobiles import Mobiles as Model_mobiles
import hashlib

class ViewCommerce(ResourceHandler):
    decorators = [
        auth.require_auth_session,
    ]

    def get(self, id=0):
        if id == 0:
            result = Model_commerce.get_all()
            array = []
            
            if len(result) > 0:
                for list_result in result:
                    array_mobil = []
                    for list_key_mobiles in list_result['mobiles']:
                        print("list_key_mobiles", list_key_mobiles)
                        result_mobiles = Model_mobiles.get_by_id(list_key_mobiles)
                        print("result_mobiles", result_mobiles)
                        if result_mobiles is not None:
                            array_mobil.append({
                                "model": result_mobiles['model'],
                                "state": result_mobiles['state'],
                                "mac": result_mobiles['mac']                                
                            })
                    json = {
                        "key": list_result['key'],
                        "name": list_result['name'],
                        "address": list_result['address'],
                        "code": list_result['code'],
                        "mobiles": array_mobil
                    }
                    array.append(json)
                return Rest.response(200, HttpStatus.OK, array)
            else:
                return Rest.response(400, HttpStatus.DEFAULT_ERROR_MESSAGE, {'reason': 'Model_commerce are empty'})
        else:
            result = Model_commerce.get_by_id(id)
            if result is not None:
                    return Rest.response(200, HttpStatus.OK, result)
            else:
                return Rest.response(400, HttpStatus.RESOURCE_NOT_EXIST)
    
    @auth.has_role_of("SUPER_ADMIN", "GENERAL_ADMINISTRATOR")
    @Auth.validate_request("name", "name", "mobiles")
    def post(self):
        content = request.get_json()
        name = content.get('name', None)
        address = content.get('address', None)
        mobiles = content.get('mobiles', None)

        try:
            _new_mobiles = Model_commerce()
            _new_mobiles.name = name
            _new_mobiles.address = address
            _new_mobiles.mobiles = mobiles
            Model_commerce.save(_new_mobiles)
            return Rest.response(200, HttpStatus.OK, {'message': 'commerce created successfully!'})
        except Exception as e:
            print ("usersView POST Exception:", e)
            return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, {'reason': str(e)})
    @auth.has_role_of("SUPER_ADMIN", "GENERAL_ADMINISTRATOR")
    def put(self, id=0):
        if id == 0:
            return Rest.response(400, HttpStatus.DEFAULT_ERROR_MESSAGE, {'reason': 'use ID and retry again'})
        else:
            content = request.get_json()
            name = content.get('name', None)
            address = content.get('address', None)
            mobiles = content.get('mobiles', None)
            

            try:
                rol_to_find = Model_commerce.get_by_id(id)
                rol_to_find['name'] = name
                rol_to_find['address'] =  address
                rol_to_find['mobiles'] = mobiles
                result = Model_commerce.update(id, rol_to_find)

                if result is None:
                    return Rest.response(200, HttpStatus.OK, {'message': 'commerce updated successfully!'})
                else:
                    print("update_doc result error:", result)
                    return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, {'reason': str(result)})

            except Exception as e:
                print ("RoleView POST Exception:", e)
                return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, {'reason': str(e)})
    @auth.has_role_of("SUPER_ADMIN", "GENERAL_ADMINISTRATOR")
    def delete(self, id=None):
        if id is None:
            return Rest.response(400, HttpStatus.DEFAULT_ERROR_MESSAGE, {'reason': 'use ID and retry again'})
        else:
            result = Model_commerce.delete(id)
            if result is None:
                return Rest.response(200, HttpStatus.OK, {'message': 'Rol delete successfully!'})
            else:
                print("delete result error:", result)
                return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, {'reason': str(result)})

