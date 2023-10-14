# -*- coding: utf-8 -*-

from app.ext.rest import consumer
from app.config.cartodb import CARTODB_URI, CARTODB_ACCOUNT, CARTODB_API_KEY
import logging as log


carto_api_config = {
    'uri': CARTODB_URI.format(CARTODB_ACCOUNT),
    'key': CARTODB_API_KEY,
}


def sql_api(sql=None):
    if sql is None:
        return None

    params = {
        'api_key': carto_api_config['key'],
        'q': sql
    }

    resp = consumer(carto_api_config['uri'], 'POST', params, use_ssl=True)

    if resp is None:
        log.info("cartodb result none")
        return None
    else:
        if 'rows' in resp:
            log.info("cartodb result success")
            return resp
        elif 'error' in resp:
            log.warning("cartodb result error")
            return resp
