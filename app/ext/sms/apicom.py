# -*- coding: utf-8 -*-

import xml.etree.ElementTree as xmlTree
from app.config.sms import APICOM_URL_API, APICOM_USERNAME_API, APICOM_PASSWORD_API
from app.ext.rest import consumer
from app.ext.utils import Commons
import logging as log
from urllib.parse import quote

sms_key_list = ('country', 'mobile', 'message')
basel_url = "{0}transaction_type={1}&user_id={2}&user_pw={3}&product_id={4}&number={5}&msg={6}"
TRANSACTION_TYPE = 400
PRODUCT_ID = 3237


class ApiCOMSMS:

    @staticmethod
    def single_sms(message_data=None):

        if message_data is None:
            log.warning("ApiCOMSMS: missing fields 'message_data'")
            return None

        if type(message_data) is not dict:
            log.warning("ApiCOMSMS: fields 'message_data' is not a dict")
            return None

        if all(param in message_data for param in sms_key_list):
            print("ApiCOMSMS: param in message_data:", message_data)
            try:
                number = "{0}{1}".format(message_data['country'], message_data['mobile'])

                quote_msg = quote(message_data['message'])

                default_message = basel_url.format(APICOM_URL_API, TRANSACTION_TYPE, APICOM_USERNAME_API, APICOM_PASSWORD_API, PRODUCT_ID, number, quote_msg)

                resp = consumer(default_message, 'GET', use_ssl=True)
                # print("ApiCOMSMS: response consumer", resp)

                if b'Transaction accepted' in resp:
                    print("ApiCOMSMS: Transaction accepted")
                    return None
                else:
                    print("ApiCOMSMS: An error occurred ", resp)
                    return "An error occurred: {0}".format(resp)
            except Exception as e:
                log.warning("ApiCOMSMS: single_sms Exception", e)
                return str(e)

        else:
            log.warning("ApiCOMSMS: missing fields in 'message_data': %s", str(sms_key_list))
            return None

    @staticmethod
    def masive_sms(message_list=200):

        if message_list is None:
            log.warning("AldeamoSMS: missing fields 'message_list'")
            return None

        if type(message_list) is not dict:
            log.warning("AldeamoSMS: fields 'message_list' is not a dict")
            return None

        if all(param in message_list for param in sms_key_list):
            mobile_list = message_list['mobile']

            if Commons.is_iterable(mobile_list):
                if len(mobile_list) > 0:
                    default_message = """
                        <sending>
                            <authentication>
                                <username>{0}</username>
                                <password>{1}</password>
                            </authentication>
                            <country>{2}</country>
                        </sending>
                    """.format(APICOM_USERNAME_API, APICOM_PASSWORD_API, message_list['country'])

                    try:
                        xml_root = xmlTree.fromstring(default_message)
                        recipients = xmlTree.SubElement(xml_root, 'recipients')

                        for phone in mobile_list:
                            sms = xmlTree.SubElement(recipients, 'sms')

                            mobile = xmlTree.SubElement(sms, 'mobile')
                            mobile.text = phone

                            message = xmlTree.SubElement(sms, 'message')
                            new_sms = message_list['message']
                            # _sms = message_list['message']
                            # new_sms = _sms.encode('latin-1', 'ignore').strip()
                            message.text = new_sms

                        str_xml = xmlTree.tostring(xml_root, encoding='ISO-8859-1', method='xml')

                        try:
                            resp = consumer(APICOM_URL_API, 'POST', str_xml, headers, use_ssl=True, options='xml')
                            print("Aldeamo Response", resp)
                            return resp
                        except Exception as e:
                            print("Aldeamo consumer Exception", e)
                            log.warning("Aldeamo consumer Exception", e)
                            return str(e)

                    except Exception as e:
                        log.warning("AldeamoSMS Exception: %s", str(e))
                        return str(e)
                else:
                    log.warning("AldeamoSMS: fields 'mobile_list' is empty")
                    return None
            else:
                log.warning("AldeamoSMS: 'mobile_list' is not iterable")
                return None
        else:
            log.warning("AldeamoSMS: missing fields in 'message_list': %s", str(sms_key_list))
            return None
