# -*- coding: utf-8 -*-

from app.ext.rest import consumer
from app.config.sitidata import GEOASSISTED

assisted_config = {
    'uri': GEOASSISTED['url'],
}


def geoassisted(data):
    if data is None:
        return None

    if 'city' not in data:
        return None
    if 'address' not in data:
        return None

    form_data = {
        "city": data['city'],
        "address": data['address'],
        "usr": GEOASSISTED['user'],
        "pwd": GEOASSISTED['passwd'],
        "parameters": GEOASSISTED['chain_geo']
    }

    resp = consumer(assisted_config['uri'], 'POST', form_data)

    if resp is None:
        return None
    else:
        if 'data' in resp:
            return resp['data']
        else:
            return resp
