from flask import request
from app.ext.security import Auth
from app.ext.security.auth_cached import Auth as auth
from app.ext.rest import Rest, HttpStatus
from app.ext.resource_handler import ResourceHandler
from app.users.models.Users import Users as Model_users
import hashlib

class ViewUsers(ResourceHandler):
    decorators = [
        auth.require_auth_session,
    ]

    def get(self, id=0):
        if id == 0:
            result = Model_users.get_all()
            array = []
            if len(result) > 0:
                for list_result in result:
                    json = {
                        "key": list_result['key'],
                        "name_user_role": list_result['name_user_role'],
                        "username": list_result['username']
                    }
                    array.append(json)
                return Rest.response(200, HttpStatus.OK, array)
            else:
                return Rest.response(400, HttpStatus.DEFAULT_ERROR_MESSAGE, {'reason': 'Model_users are empty'})
        else:
            result = Model_users.get_by_id(id)
            if result is not None:
                    return Rest.response(200, HttpStatus.OK, result)
            else:
                return Rest.response(400, HttpStatus.RESOURCE_NOT_EXIST)
    
    @auth.has_role_of("SUPER_ADMIN", "GENERAL_ADMINISTRATOR")
    @Auth.validate_request("username")
    def post(self):
        content = request.get_json()
        username = content.get('username', None)
        password = content.get('password', None)
        name_user_role = content.get('name_user_role', None)
        role_id = content.get('role_id', None)

        try:
            _new_users = Model_users()
            _new_users.username = username
            _new_users.password = hashlib.sha256(str(password).encode('utf-8')).hexdigest()
            _new_users.name_user_role = name_user_role
            _new_users.role_id = role_id
            Model_users.save(_new_users)
            return Rest.response(200, HttpStatus.OK, {'message': 'users created successfully!'})
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
            password = hashlib.sha256(str(content.get(' password', None)).encode('utf-8')).hexdigest()
            name_user_role = content.get('name_user_role', None)
            role_id = content.get('role_id', None)
            content = request.get_json()
            

            try:
                rol_to_find = Model_users.get_by_id(id)
                rol_to_find['name'] = name
                rol_to_find['password'] =  password
                rol_to_find['name_user_role'] = name_user_role
                rol_to_find['role_id'] = role_id
                result = Model_users.update(id, rol_to_find)

                if result is None:
                    return Rest.response(200, HttpStatus.OK, {'message': 'Role updated successfully!'})
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
            result = Model_users.delete(id)
            if result is None:
                return Rest.response(200, HttpStatus.OK, {'message': 'Rol delete successfully!'})
            else:
                print("delete result error:", result)
                return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, {'reason': str(result)})

