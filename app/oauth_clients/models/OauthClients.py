# -*- coding: utf-8 -*-

from app.ext.firebase.firestore_model import FirestoreModel
from app.ext.utils import DateUtils


class OauthClients(FirestoreModel):
    __tablename__ = 'OauthClients'
    name = None
    description = None
    created_at = DateUtils.get_timestamp()
    updated_at = DateUtils.get_timestamp()
