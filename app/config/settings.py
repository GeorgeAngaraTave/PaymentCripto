# -*- coding: utf-8 -*-

"""
settings for Cl4ptr4p project.

Using Flask 1.0.2.

For more information on this file, see
README.md
"""

# Application definition
APP_VERSION = '3.a'

INSTALLED_MODULES = [
    'home',
    'auth',
    'oauth_clients',
    'roles',
    'users',
    'companies',
    'mobiles',
    'commerce',
    'uploads',
    'crypto',
    'reports'
]

# Secret key for signing cookies
SECRET_KEY = '\x10\xc8\xd9`\x90{x\xc2\xc9\x83(\xd6\xf9@\xce\xe5\x1e\x03B\x03\xc7d\xee\xfb\xe6\xe6g\xc8Il\xa6\x8a'

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "dya1sdcl4pth2tr4pcbo7uyz"

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True
