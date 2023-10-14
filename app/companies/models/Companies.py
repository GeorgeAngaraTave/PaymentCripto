# -*- coding: utf-8 -*-

from app.ext.firebase.firestore_model import FirestoreModel
from app.ext.utils import DateUtils


class Companies(FirestoreModel):
    __tablename__ = 'Companies'
    name = None
    provider_code = None
    status = None
    created_at = DateUtils.get_timestamp()
    updated_at = DateUtils.get_timestamp()
