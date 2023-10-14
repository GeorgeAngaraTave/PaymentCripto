# -*- coding: utf-8 -*-

from app.ext.firebase.firestore_model import FirestoreModel
from app.ext.utils import DateUtils


class Users(FirestoreModel):
    __tablename__ = 'Users'
    username = None
    password = None
    created_at = DateUtils.get_timestamp()
    updated_at = DateUtils.get_timestamp()
