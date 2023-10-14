# -*- coding: utf-8 -*-

# Mail Settings
# For more information, see app.ext.mail module

# configurations for email on custom server
import os

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
DEFAULT_MAIL_SENDER = os.environ.get('DEFAULT_MAIL_SENDER', 'lilith@awesomeapp.com')
MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'lilith@awesomeapp.com')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'awesome_passwd')
MAIL_USE_TLS = False
MAIL_USE_SSL = True

# administrator mail
MAIL_ADMIN = os.environ.get('MAIL_ADMIN', 'lilith@awesomeapp.com')

# configurations for sendgrid server
SENDGRID_API_KEY = 'awesome-api-key-from-sendgrid'

DEFAULT_SUBJECT_MAIL = "BackendBase Mail"

DEFAULT_MAIL_MSG = """
    Este email es generado automaticamente desde la aplicacion BackendBase
    Favor no responder.

"""
