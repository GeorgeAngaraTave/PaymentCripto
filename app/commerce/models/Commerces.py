# -*- coding: utf-8 -*-

from app.ext.firebase.firestore_model import FirestoreModel
from app.ext.utils import DateUtils


class Commerces(FirestoreModel):
    __tablename__ = 'Commerce'
    name = None
    address = None
    mobiles = None
    code = None
    created_at = DateUtils.get_timestamp()
    updated_at = DateUtils.get_timestamp()
