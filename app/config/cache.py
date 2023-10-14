# -*- coding: utf-8 -*-

from werkzeug.contrib.cache import MemcachedCache, FileSystemCache
import os
from app.config.local_settings import SESSION_EXPIRE_TIME


def init_werkzeug_cache():
    # config cache
    cache = None

    server_software = os.environ.get('GAE_ENV')
    # print("SERVER_SOFTWARE:", os.environ.get('SERVER_SOFTWARE'))
    # print("SERVER_SOFTWARE GAE_ENV:", server_software)

    # print("GAE_APPLICATION:", os.environ.get('GAE_APPLICATION'))
    # print("GAE_DEPLOYMENT_ID:", os.environ.get('GAE_DEPLOYMENT_ID'))
    # print("GAE_ENV:", os.environ.get('GAE_ENV'))
    # print("GAE_INSTANCE:", os.environ.get('GAE_INSTANCE'))
    # print("GAE_MEMORY_MB:", os.environ.get('GAE_MEMORY_MB'))
    # print("GAE_RUNTIME:", os.environ.get('GAE_RUNTIME'))
    # print("GAE_SERVICE:", os.environ.get('GAE_SERVICE'))
    # print("GAE_VERSION:", os.environ.get('GAE_VERSION'))
    # print("GOOGLE_CLOUD_PROJECT:", os.environ.get('GOOGLE_CLOUD_PROJECT'))
    # print("NODE_ENV:", os.environ.get('NODE_ENV'))
    # print("PORT:", os.environ.get('PORT'))

    if server_software is None:
        # on filesystem
        print("setup cache on filesystem")
        cache = FileSystemCache('/tmp', default_timeout=SESSION_EXPIRE_TIME)
        # cache = MemcachedCache()
        return cache

    if 'standar' in server_software:
        # on GAE
        print("setup cache on GAE 2nd Gen")
        # cache = MemcachedCache()
        cache = FileSystemCache('/tmp', default_timeout=SESSION_EXPIRE_TIME)
        return cache

    if server_software.startswith(('development', 'Development', 'testutil', 'gunicorn')):
        # on GAE Local
        print("setup cache on GAE LOCAL Server")
        cache = FileSystemCache('/tmp', default_timeout=SESSION_EXPIRE_TIME)
        # cache = MemcachedCache()
        return cache
