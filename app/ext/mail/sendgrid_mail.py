# -*- coding: utf-8 -*-

import sendgrid
from sendgrid.helpers import mail
from sendgrid.helpers.mail import Mail, Email, Personalization, Content
from app.config.mail import DEFAULT_MAIL_MSG, DEFAULT_SUBJECT_MAIL
from app.config.mail import SENDGRID_API_KEY, MAIL_ADMIN
from app.ext.utils import Commons
import logging as log


class SendGridMail(object):

    @staticmethod
    def sendgrid_email(message_body=None, recipient=None):
        if message_body is None:
            log.warning("SendGrid sendEmail: The message can not be sent blank")
            return None

        if recipient is None:
            log.warning("SendGrid sendEmail: The mailing list can not be empty")
            return None

        if Commons.validate_email(recipient):
            try:
                sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)

                from_email = mail.Email(MAIL_ADMIN)
                to_email = mail.Email(recipient)

                content = mail.Content('text/plain', DEFAULT_MAIL_MSG + message_body)
                message = mail.Mail(from_email, DEFAULT_SUBJECT_MAIL, to_email, content)

                response = sg.client.mail.send.post(request_body=message.get())
                return response
            except Exception, e:
                log.warning("SendGrid sendEmail Exception: %s", str(e))
                return None

    @staticmethod
    def sendgrid_massive_email(message_body=None, recipient_list=None):
        if message_body is None:
            log.warning("SendGrid sendgrid_massive_email: The message can not be sent blank")
            return None

        if recipient_list is None:
            log.warning("SendGrid sendgrid_massive_email: The mailing list, can not be empty")
            return None

        if Commons.is_iterable(recipient_list):
            if len(recipient_list) > 0:
                try:
                    sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)

                    email = Mail()
                    email.from_email = Email(MAIL_ADMIN)
                    email.subject = DEFAULT_SUBJECT_MAIL

                    personalization = Personalization()

                    for emails in recipient_list:
                        personalization.add_to(Email(emails))

                    email.add_personalization(personalization)
                    email.add_content(Content("text/plain", DEFAULT_MAIL_MSG + message_body))

                    data = email.get()

                    response = sg.client.mail.send.post(request_body=data)

                    return response

                except Exception, e:
                    log.warning("SendGrid sendgrid_massive_email Exception: %s", str(e))
                    return None
            else:
                log.warning("SendGrid sendgrid_massive_email: recipient_list: is empty")
                return None
        else:
            log.warning("SendGrid sendgrid_massive_email: recipient_list is not a list")
            return None
