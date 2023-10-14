# -*- coding: utf-8 -*-

from app.ext.rest import consumer
from geo_status import status_geo
from app.config.sitidata import GEOREVERSED


georeversed_config = {
    'uri': GEOREVERSED['url'],
    'token': GEOREVERSED['token'],
}

headers = {
    'Authorization': 'Token ' + georeversed_config['token']
}


def georeversed(data):
    if data is None:
        return None

    if len(data) <= 0:
        return None

    resp = consumer(georeversed_config['uri'], 'POST', data, headers)

    if resp is None:
        return None
    else:
        if 'data' in resp:
            item = resp['data']
            item['status'] = status_geo(item['status'])
            return resp['data']
        else:
            return resp
