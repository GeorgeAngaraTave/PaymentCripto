from flask import request
from app.ext.security import Auth
from app.ext.rest import Rest, HttpStatus
from app.ext.resource_handler import ResourceHandler
from app.companies.models.Companies import Companies


class ViewCompanies(ResourceHandler):
    # decorators = [
    #     Auth.require_user_session,
    # ]

    def get(self, id=0):
        if id == 0:
            result = Companies.get_all()
            if len(result) > 0:
                return Rest.response(200, HttpStatus.OK, result)
            else:
                return Rest.response(400, HttpStatus.DEFAULT_ERROR_MESSAGE, {'reason': 'Companies are empty'})
        else:
            result = Companies.get_by_id(id)
            if result is not None:
                return Rest.response(200, HttpStatus.OK, result)
            else:
                return Rest.response(400, HttpStatus.RESOURCE_NOT_EXIST)

    @Auth.validate_request("name", "provider_code")
    def post(self):
        content = request.get_json()
        name = content.get('name', None)
        provider_code = content.get('provider_code', None)
        status = content.get('status', True)

        try:
            _new_company = Companies()
            _new_company.name = name
            _new_company.provider_code = provider_code
            _new_company.status = status
            result = Companies.save(_new_company)

            if result is None:
                return Rest.response(200, HttpStatus.OK, {'message': 'Company created successfully!'})
            else:
                return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, {'reason': str(result)})
        except Exception as e:
            print ("ViewCompanies POST Exception:", e)
            return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, {'reason': str(e)})

    @Auth.validate_request("name", "provider_code")
    def put(self, id=None):
        if id is None:
            return Rest.response(400, HttpStatus.DEFAULT_ERROR_MESSAGE, {'reason': 'use a company ID and retry again'})
        else:
            content = request.get_json()
            name = content.get('name', None)
            provider_code = content.get('provider_code', None)
            status = content.get('status', None)

            try:
                company_to_find = Companies.get_by_id(id)

                if company_to_find is not None:
                    company_to_find['name'] = name if name else company_to_find['name']
                    company_to_find['provider_code'] = provider_code if provider_code else company_to_find['provider_code']
                    company_to_find['status'] = status if status else company_to_find['status']

                    result = Companies.update(id, company_to_find)

                    if result is None:
                        return Rest.response(200, HttpStatus.OK, {'message': 'Company updated successfully!'})
                    else:
                        print("Company update_doc result error:", result)
                        return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, {'reason': str(result)})
                else:
                    return Rest.response(400, HttpStatus.RESOURCE_NOT_EXIST)

            except Exception as e:
                print("CompaniesView PUT Exception:", e)
                return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, {'reason': str(e)})

    def delete(self, id=None):
        if id is None:
            return Rest.response(400, HttpStatus.DEFAULT_ERROR_MESSAGE, {'reason': 'use a company ID and retry again'})
        else:
            result = Companies.delete(id)

            if result is None:
                return Rest.response(200, HttpStatus.OK, {'message': 'Company delete successfully!'})
            else:
                print("delete result error:", result)
                return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, {'reason': str(result)})


