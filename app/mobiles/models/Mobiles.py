# -*- coding: utf-8 -*-

from app.ext.firebase.firestore_model import FirestoreModel
from app.ext.utils import DateUtils


class Mobiles(FirestoreModel):
    __tablename__ = 'MOBILE'
    model = None
    state = None
    mac = None
    created_at = DateUtils.get_timestamp()
    updated_at = DateUtils.get_timestamp()
