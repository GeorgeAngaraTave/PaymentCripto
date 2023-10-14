# -*- coding: utf-8 -*-

# Sitidata Settings
# For more information, see app.ext.servinf module
import os

GEOCODER = {
    'url': 'https://sitidata-stdr.appspot.com/api/geocoder/',
    'token': os.environ.get('GEOCODER_TOKEN', 'awesome_geocoder_token'),
}

GEOMASSIVE = {
    'url': 'https://sitidata-stdr.appspot.com/api/massive',
    'url_alt': 'https://sitidata-stdr.appspot.com/api/outobjmassive',
    'token': os.environ.get('GEOMASSIVE_TOKEN', 'awesome_geomassive_token')
}

GEOASSISTED = {
    'url': 'http://104.154.77.207/webservices/geoassisted',
    'user': os.environ.get('GEO_USER', 'awesome_user'),
    'passwd': os.environ.get('GEO_PASWD', 'awesome_paswd'),
    'chain_geo': os.environ.get('GEO_CHAIN', 'awesome_chain_geo'),
}

GEOREVERSED = {
    'url': 'https://sitidata-stdr.appspot.com/api/geoinverso',
    'token': os.environ.get('GEOREVERSED_TOKEN', 'awesome_georeversed_token')
}
