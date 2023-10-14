from flask import request
from app.ext.security import Auth
from app.roles.models.Roles import Roles
from app.ext.security.auth_cached import Auth as auth
from app.ext.rest import Rest, HttpStatus
from app.ext.resource_handler import ResourceHandler


class ViewRoles(ResourceHandler):
    decorators = [
        auth.require_auth_session,
    ]

    def get(self, id=0):
        if id == 0:
            result = Roles.get_all()
            if len(result) > 0:
                return Rest.response(200, HttpStatus.OK, result)
            else:
                return Rest.response(400, HttpStatus.DEFAULT_ERROR_MESSAGE, {'reason': 'Roles are empty'})
        else:
            result = Roles.get_by_id(id)
            if result is not None:
                    return Rest.response(200, HttpStatus.OK, result)
            else:
                return Rest.response(400, HttpStatus.RESOURCE_NOT_EXIST)

    @auth.has_role_of("SUPER_ADMIN")
    @Auth.validate_request("name")
    def post(self):
        content = request.get_json()
        name = content.get('name', None)
        description = content.get('description', None)

        try:
            _new_role = Roles()
            _new_role.name = name
            _new_role.description = description
            Roles.save(_new_role)
            return Rest.response(200, HttpStatus.OK, {'message': 'Role created successfully!'})
        except Exception as e:
            print ("RoleView POST Exception:", e)
            return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, {'reason': str(e)})
    @auth.has_role_of("SUPER_ADMIN")
    def put(self, id=0):
        if id == 0:
            return Rest.response(400, HttpStatus.DEFAULT_ERROR_MESSAGE, {'reason': 'use ID and retry again'})
        else:
            content = request.get_json()
            name = content.get('name', None)
            description = content.get('description', None)

            try:
                rol_to_find = Roles.get_by_id(id)
                rol_to_find['name'] = name
                rol_to_find['description'] = description
                result = Roles.update(id, rol_to_find)

                if result is None:
                    return Rest.response(200, HttpStatus.OK, {'message': 'Role updated successfully!'})
                else:
                    print("update_doc result error:", result)
                    return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, {'reason': str(result)})

            except Exception as e:
                print ("RoleView POST Exception:", e)
                return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, {'reason': str(e)})
    @auth.has_role_of("SUPER_ADMIN")
    def delete(self, id=None):
        if id is None:
            return Rest.response(400, HttpStatus.DEFAULT_ERROR_MESSAGE, {'reason': 'use ID and retry again'})
        else:
            result = Roles.delete(id)
            if result is None:
                return Rest.response(200, HttpStatus.OK, {'message': 'Rol delete successfully!'})
            else:
                print("delete result error:", result)
                return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, {'reason': str(result)})

