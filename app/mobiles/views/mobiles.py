from flask import request
from app.ext.security import Auth
from app.ext.security.auth_cached import Auth as auth
from app.ext.rest import Rest, HttpStatus
from app.ext.resource_handler import ResourceHandler
from app.users.models.Users import Users as Model_users
from app.mobiles.models.Mobiles import Mobiles as Model_mobiles
import hashlib

class ViewMobiles(ResourceHandler):
    decorators = [
        auth.require_auth_session,
    ]

    def get(self, id=0):
        if id == 0:
            result = Model_mobiles.get_all()
            array = []
            #print(result)
            
            if len(result) > 0:
                for list_result in result:
                    json = {
                        "key": list_result['key'],
                        "model": list_result['model'],
                        "state": list_result['state'],
                        "mac": list_result['mac']
                    }
                    array.append(json)
                return Rest.response(200, HttpStatus.OK, array)
            else:
                return Rest.response(400, HttpStatus.DEFAULT_ERROR_MESSAGE, {'reason': 'Model_mobiles are empty'})
        else:
            result = Model_users.get_by_id(id)
            if result is not None:
                    return Rest.response(200, HttpStatus.OK, result)
            else:
                return Rest.response(400, HttpStatus.RESOURCE_NOT_EXIST)
    
    @auth.has_role_of("SUPER_ADMIN", "GENERAL_ADMINISTRATOR")
    @Auth.validate_request("model", "mac", "state")
    def post(self):
        content = request.get_json()
        model = content.get('model', None)
        mac = content.get('mac', None)
        state = content.get('state', None)

        try:
            _new_mobiles = Model_mobiles()
            _new_mobiles.model = model
            _new_mobiles.mac = mac
            _new_mobiles.state = state
            Model_mobiles.save(_new_mobiles)
            return Rest.response(200, HttpStatus.OK, {'message': 'mobiles created successfully!'})
        except Exception as e:
            print ("usersView POST Exception:", e)
            return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, {'reason': str(e)})
    @auth.has_role_of("SUPER_ADMIN", "GENERAL_ADMINISTRATOR")
    def put(self, id=0):
        if id == 0:
            return Rest.response(400, HttpStatus.DEFAULT_ERROR_MESSAGE, {'reason': 'use ID and retry again'})
        else:
            content = request.get_json()
            model = content.get('model', None)
            mac = content.get('mac', None)
            state = content.get('state', None)
            

            try:
                rol_to_find = Model_mobiles.get_by_id(id)
                rol_to_find['model'] = model
                rol_to_find['mac'] =  mac
                rol_to_find['state'] = state
                result = Model_mobiles.update(id, rol_to_find)

                if result is None:
                    return Rest.response(200, HttpStatus.OK, {'message': 'Mobiles updated successfully!'})
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
            result = Model_mobiles.delete(id)
            if result is None:
                return Rest.response(200, HttpStatus.OK, {'message': 'Rol delete successfully!'})
            else:
                print("delete result error:", result)
                return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, {'reason': str(result)})

