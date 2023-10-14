from flask import request
from app.ext.security import Auth
from app.ext.security.auth_cached import Auth as auth
from app.ext.rest import Rest, HttpStatus
from app.ext.resource_handler import ResourceHandler
from app.oauth_clients.models.OauthClients import OauthClients


class ViewOauthClients(ResourceHandler):
    decorators = [
        auth.require_auth_session,
    ]

    def get(self, id=0):
        if id == 0:
            result = OauthClients.get_all()
            if len(result) > 0:
                return Rest.response(200, HttpStatus.OK, result)
            else:
                return Rest.response(400, HttpStatus.DEFAULT_ERROR_MESSAGE, {'reason': 'OauthClients are empty'})
        else:
            result = OauthClients.get_by_id(id)
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
            _new_oauth_client = OauthClients()
            _new_oauth_client.name = name
            _new_oauth_client.description = description
            OauthClients.save(_new_oauth_client)
            return Rest.response(200, HttpStatus.OK, {'message': 'OauthClients created successfully!'})
        except Exception as e:
            print ("OauthClientsView POST Exception:", e)
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
                oauth_client_to_find = OauthClients.get_by_id(id)
                oauth_client_to_find['name'] = name
                oauth_client_to_find['description'] = description
                result = OauthClients.update(id, oauth_client_to_find)

                if result is None:
                    return Rest.response(200, HttpStatus.OK, {'message': 'OauthClients updated successfully!'})
                else:
                    print("update_doc result error:", result)
                    return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, {'reason': str(result)})

            except Exception as e:
                print ("OauthClientsView POST Exception:", e)
                return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, {'reason': str(e)})

    @auth.has_role_of("SUPER_ADMIN")
    def delete(self, id=None):
        if id is None:
            return Rest.response(400, HttpStatus.DEFAULT_ERROR_MESSAGE, {'reason': 'use ID and retry again'})
        else:
            result = OauthClients.delete(id)
            if result is None:
                return Rest.response(200, HttpStatus.OK, {'message': 'OauthClients delete successfully!'})
            else:
                print("delete result error:", result)
                return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, {'reason': str(result)})

