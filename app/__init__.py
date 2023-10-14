# -*- coding: utf-8 -*-

import sys
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS

from .config.databases.settings import DATABASE_CONNECTION
from .config.local_settings import ALLOW_METHODS, USE_STDERR
from .config.storage import MAX_FILE_SIZE, DEFAULT_BUCKET
from .config.settings import SECRET_KEY
from .config.cache import init_werkzeug_cache


app = Flask(__name__)

app.config.update(dict(
    SECRET_KEY=SECRET_KEY,
    MAX_CONTENT_LENGTH=MAX_FILE_SIZE,
    UPLOAD_FOLDER=DEFAULT_BUCKET,
))

# setup cache
cache = init_werkzeug_cache()

api = Api(app)

db = None
SQLALCHEMY_DATABASE_URI = DATABASE_CONNECTION

if DATABASE_CONNECTION is not None:
    app.config.update(dict(
        SQLALCHEMY_ECHO=False,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_DATABASE_URI=SQLALCHEMY_DATABASE_URI,
    ))
    db = SQLAlchemy(app)

# dbsession = db.session
cors = CORS(app, resources={r"/api/*": {"allow_headers": "*", "supports_credentials": "true", "max_age": 1, "methods": ALLOW_METHODS}})

# register modules
from app.ext.register import Register
reg_api = Register()

if USE_STDERR:
    logging.basicConfig(stream=sys.stderr)
