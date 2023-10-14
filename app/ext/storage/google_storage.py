# -*- coding: utf-8 -*-

import os
from google.cloud import storage, exceptions
from werkzeug.utils import secure_filename
from app.config.storage import DEFAULT_BUCKET, store_file_path
from app.ext.utils import DateUtils
from app.uploads.models.Upload import Uploads
from io import BytesIO
import logging as log

DEFAULT_FOLDER = 'general'

try:
    # Instantiates a client
    storage_client = storage.Client()
except Exception as e:
    print("Google Storage Client Exception:", e)
    raise e


class StorageFile():

    @staticmethod
    def save_logs(data=None):

        if data is None:
            return None

        try:
            _new_data = Uploads()
            _new_data.original_name = data['original_name']
            _new_data.generated_name = data['generated_name']
            _new_data.bucket_path = data['bucket_path']
            _new_data.is_public = data['is_public']

            Uploads.save(_new_data)

        except Exception as e:
            log.warning("An error occurred while saving the info file to Firestore.")
            log.warning("StorageFile save_logs Exception:", e)

        return None

    def get_default_bucket():
        try:
            default_bucket = storage_client.get_bucket(DEFAULT_BUCKET)
            return default_bucket
        except exceptions.NotFound as e:
            print("StorageFile get_default_bucket Exception:", e)
        return None

    @staticmethod
    def save_file(file_name=None, blob_content=None, file_content_type=None, meta_data=None, folder_path=None, make_public=False, save_log=True):

        if file_name is None:
            return None

        if blob_content is None:
            return None

        if file_content_type is None:
            return None

        new_filename = None

        try:
            filename, ext = os.path.splitext(file_name)
            new_filename = "{0}_{1}{2}".format(filename, DateUtils.get_timestamp(), ext)
        except Exception as e:
            new_filename = "{0}_{1}".format(DateUtils.get_timestamp(), file_name)

        if folder_path is None:
            store_file_path = "{0}/{1}".format(DEFAULT_FOLDER, secure_filename(new_filename))
        else:
            store_file_path = "{0}/{1}".format(folder_path, secure_filename(new_filename))

        try:
            bucket = StorageFile.get_default_bucket()

            if bucket:
                blob = bucket.blob(store_file_path)
                blob.upload_from_string(blob_content, content_type=file_content_type)

                if meta_data is not None:
                    blob.metadata = meta_data
                    # update metadata
                    blob.patch()

                if make_public is True:
                    blob.make_public()

                # print('Blob {} is publicly accessible at {}'.format(blob.name, blob.public_url))

                if save_log is True:
                    StorageFile.save_logs({
                        'original_name': file_name,
                        'generated_name': store_file_path,
                        'bucket_path': blob.public_url,
                        'is_public': make_public
                    })

                return {
                    'storage_id': blob.id,
                    'url': blob.public_url,
                }
            else:
                return {
                    'error': "Unexpected Error: Bucket '{0}', Not Found".format(DEFAULT_BUCKET)
                }
        except Exception as e:
            log.warning("An error occurred while saving the file to gcs.")
            log.warning("StorageFile save_file Exception: {0}".format(str(e)))

            return {
                'error': str(e)
            }

    @staticmethod
    def get_file(self, filename):

        if filename is None:
            return None

        bucket = StorageFile.get_default_bucket()
        store_file = store_file_path + filename

        blob = bucket.blob(store_file)

        string_buffer = BytesIO()
        blob.download_to_file(string_buffer)
        content = string_buffer.getvalue()
        return content
