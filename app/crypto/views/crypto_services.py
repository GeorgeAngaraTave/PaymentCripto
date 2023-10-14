# -*- coding: utf-8 -*-

from app.ext.rest import consumer
from app.ext.rest import Rest, HttpStatus
from app.config.local_settings import CRYPTO_PROJECT 
import requests
import os

def generate_token():
    try:
        headers = {
            'Content-Type': 'application/json'
        } 
        
        resp = consumer(CRYPTO_PROJECT['TOKEN'], 'GET', None, headers)    
        #resp = consumer(assisted_config['uri'], 'POST', form_data)        
        if resp is None:
            return None
        else:
            return resp
    except Exception as e:
        print("CompaniesView POST Exception:", e)
        return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, {'reason': str(e)})


def cop_value(amount, name, token, operation):
    try:
        headers = {
            'Content-Type': 'application/json',
            'auth': str(token['auth'])
        } 

        crypto_type = {
                'LITECOIN': 'LTC',
                'BITCOIN': 'BTC'
        } 
        
        if operation == 'CRYPTO':
            complement = '?from=COP&to='+crypto_type[str(name)]+'&amount='+str(amount)
            #'from=LTC&to=COP&amount='+str(amount)
        else:
            complement = '?from='+crypto_type[str(name)]+'&to=COP&amount='+str(amount)


        URL = CRYPTO_PROJECT['BITCOIN']+complement
        resp = consumer(URL, 'GET', None, headers) 
        #resp = consumer(assisted_config['uri'], 'POST', form_data)        
        if resp is None:
            return None
        else:
            return resp
    except Exception as e:
        print("CompaniesView POST Exception:", e)
        return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, {'reason': str(e)})


def crypto_transation(data, token):
    try:
        # headers = {
        #     'Content-Type': 'application/json',
        #     'auth': str(token['auth'])
        # } 
        
        #URL = CRYPTO_PROJECT['TRANSATION_'+data['crypto_name']]+'?from='+str(data['adress_from'])+'&to='+str(data['adress_to'])+'&amount='+str(data['amount'])
        #print('URL', URL)
        URL = CRYPTO_PROJECT['TRANSATION_'+data['crypto_name']]
        #print('URL', URL)
        json_ = {
            "from": str(data['adress_from']),
            "to": str(data['adress_to']),
            "amount": data['amount']      
        }
        # print('json_++++', json_)
        #resp = consumer(URL, 'POST', json_, headers)  
        url = URL 
        payload = json_ 
        headers = {
            'Content-Type': 'application/json',
            'auth': str(token['auth'])
        }
        response = requests.post(url, headers = headers, json = payload) 
        #print('requests.post **', response.json())  
        return response.json()   
        # if resp is None:
        #     return None
        # else:
        #     return resp
    except Exception as e:
        print("CompaniesView POST Exception:", e)
        return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, {'reason': str(e)})

def get_balance(data, token):
    try:
        headers = {
            'Content-Type': 'application/json',
            'auth': str(token['auth'])
        } 
        
        URL = CRYPTO_PROJECT['BALANCE_'+data['crypto_name']]+str(data['adress_from'])+'?amount='+str(data['amount'])
        #print('URL get_balance', URL)
        resp = consumer(URL, 'GET', None, headers) 
          
        #resp = consumer(assisted_config['uri'], 'POST', form_data)        
        if resp is None:
            return None
        else:
            return resp
    except Exception as e:
        print("CompaniesView POST Exception:", e)
        return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, {'reason': str(e)})
