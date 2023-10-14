
try:
    from google_mail import sendEmail
    from sendgrid_mail import SendGridMail
except ImportError:
    import logging as log
    log.warning('Warning: google_mail module only is allowed on GAE Server')
    from custom_mail import sendEmail
