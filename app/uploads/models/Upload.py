# -*- coding: utf-8 -*-
from app.ext.firebase.firestore_model import FirestoreModel
from app.ext.utils import DateUtils


class Uploads(FirestoreModel):
    __tablename__ = 'Uploads'
    original_name = None
    generated_name = None
    bucket_path = None
    is_public = False
    status = None
    created_at = DateUtils.get_timestamp()
    updated_at = DateUtils.get_timestamp()
