from flask import request
from app.ext.resource_handler import ResourceHandler
from app.ext.security import Auth
from app.ext.rest import Rest, HttpStatus
from werkzeug.utils import secure_filename
from app.ext.utils import Commons
from app.config.storage import MAX_FILE_SIZE
from app.ext.storage import StorageFile
from app.uploads.models.Upload import Uploads


class ViewUpload(ResourceHandler):
    # decorators = [
    #     Auth.require_auth_session
    # ]

    def get(self, id=0):
        if id == 0:
            result = Uploads.get_all()
            if len(result) > 0:
                return Rest.response(200, HttpStatus.OK, result)
            else:
                return Rest.response(400, HttpStatus.DEFAULT_ERROR_MESSAGE, {'reason': 'Uploads are empty'})
        else:
            result = Uploads.get_by_id(id)
            if result is not None:
                return Rest.response(200, HttpStatus.OK, result)
            else:
                return Rest.response(400, HttpStatus.RESOURCE_NOT_EXIST)

        return Rest.response(400, HttpStatus.RESOURCE_NOT_EXIST)

    def post(self):
        if 'file' not in request.files:
            reason = 'This service is only for uploading files'
            return Rest.response(400, HttpStatus.UNAUTHORIZED, {'reason': reason})
        else:
            file_upload = request.files['file']
            params_from_request = request.form['optional_params']

            original_filename = secure_filename(file_upload.filename)
            file_content_type = file_upload.content_type
            valid_ext, ext = Commons.allowed_files(original_filename)

            try:
                if file_upload and valid_ext:
                    blob = file_upload.read()
                    file_size = len(blob)

                    check_tam = Commons.get_file_size(file_size)

                    if check_tam > MAX_FILE_SIZE:
                        reason = 'The file size exceeds the allowed limit.'
                        return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, {'reason': reason})
                    file_saved = StorageFile.save_file(original_filename, blob, file_content_type)

                    if file_saved is not None:
                        if 'url' in file_saved:
                            return Rest.response(200, HttpStatus.OK, file_saved)
                        else:
                            return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, file_saved)
                    else:
                        return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, {'reason': 'NPI'})
                else:
                    reason = 'File type is not allowed'
                    return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, {'reason': reason})
            except Exception as e:
                print("ViewUpload Exception:", e)
                return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, {'reason': str(e)})

    def put(self):
        reason = 'This service is only for uploading files'
        return Rest.response(401, HttpStatus.UNAUTHORIZED, {'reason': reason})

    def delete(self):
        reason = 'This service is only for uploading files'
        return Rest.response(401, HttpStatus.UNAUTHORIZED, {'reason': reason})
