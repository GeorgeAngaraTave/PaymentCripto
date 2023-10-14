# -*- coding: utf-8 -*-

from app.ext.firebase.firestore_model import FirestoreModel
from app.ext.utils import DateUtils


class Roles(FirestoreModel):
    __tablename__ = 'Roles'
    name = None
    description = None
    permissions = None
    created_at = DateUtils.get_timestamp()
    updated_at = DateUtils.get_timestamp()
