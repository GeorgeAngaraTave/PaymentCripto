# -*- coding: utf-8 -*-

"""Python module for Firebase Realtime Database."""

from app.ext.rest import consumer
from app.config.google.firebase import REALTIME_URI, FIREBASE_API_KEY
import logging as log

headers = {
    'access_token': FIREBASE_API_KEY
}


def realtime_api(notification_name=None, data=None):
    if data is None:
        return None
    if notification_name is None:
        return None

    # URI = REALTIME_URI.format(str(notification_name))
    URI = "https://trax-bavaria-ml.firebaseio.com/{0}/{1}.json".format(str(notification_name), data['promotion_code'])

    resp = consumer(URI, 'PATCH', data, headers, use_ssl=True)

    if resp is None:
        print(resp)
        log.info("Firebase realtime result none")
        return None
    else:
        print(resp)
        return resp
        # if 'rows' in resp:
        #     log.info("Firebase realtime result success")
        #     return resp
        # elif 'error' in resp:
        #     log.warning("Firebase realtime result error")
        #     return resp
