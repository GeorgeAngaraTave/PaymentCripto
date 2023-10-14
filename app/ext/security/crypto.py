# -*- coding: utf-8 -*-

from werkzeug.security import generate_password_hash, check_password_hash, gen_salt

import random
import base64
from uuid import uuid4
import hashlib
from datetime import datetime
from app.ext.utils import Commons
from app.config.settings import SECRET_KEY, CSRF_SESSION_KEY

hash_key = '-super-secret-key-for-backend-base-project-please-change-this-'
hash_method = 'pbkdf2:sha512'
hash_salt = 10


def generate_random_hash(int_bytes=128):
    return random.getrandbits(int_bytes)


def generate_uuid():
    return uuid4().hex


def base64_encode(text):
    return base64.b64encode(bytes(text), 'utf-8')


def base64_decode(text):
    return base64.b64decode(text, 'utf-8')


def generate_salt(cost=30):
    return gen_salt(cost)


def generate_digest(key_digest=None):
    if key_digest is None:
        return None
    return hashlib.sha512(key_digest).digest()


def generate_key_hash(user_key):
    user_digest = generate_digest(user_key)
    hash_digest = generate_digest(hash_key)
    hash_csrf = generate_digest(CSRF_SESSION_KEY)

    new_hash_key = "{0}{1}{2}{3}".format(SECRET_KEY, user_digest, hash_digest, hash_csrf)
    hashed = base64_encode(new_hash_key)

    return hashed


def cipher_password(str_key):
    sanitized_str = Commons.sanity_check(str_key, True)
    cipher_key = generate_key_hash(sanitized_str)

    return cipher_key


def generate_password(password):
    secret_key = cipher_password(password)
    password_hash = generate_password_hash(secret_key, method=hash_method, salt_length=hash_salt)

    return password_hash


def check_password(password_hash, password):
    secret_key = cipher_password(password)
    is_valid = check_password_hash(password_hash, secret_key)

    return is_valid
