# -*- coding: utf-8 -*-

from app.ext.firebase.firestore_model import FirestoreModel
from app.ext.utils import DateUtils


class TransaccionCrypto(FirestoreModel):
    __tablename__ = 'transaccion_crypto'
    ticket = None
    code_commerce = None
    network = None
    amount_sent = None
    amount_withdrawn = None
    mac_mobil = None
    key_users = None
    datetime = None
    created_at = DateUtils.get_timestamp()
    updated_at = DateUtils.get_timestamp()
