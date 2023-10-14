# -*- coding: utf-8 -*-

from app.ext.rest import consumer
from geo_status import status_geo
from app.config.sitidata import GEOCODER


geocoder_config = {
    'uri': GEOCODER['url'],
    'token': GEOCODER['token'],
}

headers = {
    'Authorization': 'Token ' + geocoder_config['token']
}


def geocoder(data):
    if data is None:
        return None

    if len(data) <= 0:
        return None

    resp = consumer(geocoder_config['uri'], 'POST', data, headers)

    if resp is None:
        return None
    else:
        if 'data' in resp:
            item = resp['data']
            item['estado'] = status_geo(item['estado'])
            return resp['data']
        else:
            return resp
