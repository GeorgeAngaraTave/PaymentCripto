# -*- coding: utf-8 -*-

from app.ext.rest import consumer
from geo_status import status_geo
from app.config.sitidata import GEOMASSIVE


massive_config = {
    'objectOnly': GEOMASSIVE['url'],
    'objectMassive': GEOMASSIVE['url_alt'],
    'token': GEOMASSIVE['token'],
}

headers = {
    'Authorization': 'Token ' + massive_config['token']
}


def geomassive(data, geo_type=None):
    if data is None:
        return None

    if len(data) <= 0:
        return None

    form_data = {
        'row': data
    }

    resp = consumer(massive_config['objectMassive'], 'POST', form_data, headers)

    if resp is None:
        return None
    else:
        if 'data' in resp:
            for item in resp['data']:
                item['estado'] = status_geo(item['estado'])
            return resp['data']
        else:
            return resp
