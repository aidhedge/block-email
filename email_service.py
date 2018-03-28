import os
import yagmail
import json

class EmailHandler(object): 
    """
    Basic class for handling email send outs. Using yagmail.
    """
    def __init__(self, to, subject):
        self._to = to
        self._subject = subject
        self._html = None
        self._text = None
        self._format = 'html' 
    
    @property
    def html(self):
        return self._html
    
    @html.setter
    def html(self,html):
        self._html = html

    def send(self):
        body = self._html
        from_addr = os.environ['MAIL_DEFAULT_SENDER']
        if not self._html and not self._text:
            return json.dumps({'status':'error', 'description':'No content in body'})
        smtp_server = os.environ['MAIL_SERVER']
        smtp_server_port = os.environ['MAIL_PORT']
        smpt_server_user = os.environ['MAIL_USERNAME']
        smpt_server_password = os.environ['MAIL_PASSWORD']
        try:
            mail = yagmail.SMTP(user=smpt_server_user, password=smpt_server_password, host=smtp_server, port=smtp_server_port, smtp_starttls=False, smtp_ssl=False)
            mail.send(
                to = self._to,
                subject = self._subject, 
                contents = body
                )
        except BaseException:
            return json.dumps({'status':'error', 'description':'Connecting to SMTP-server'})
        else:
            return json.dumps({
                    'status':'success',
                    'recipient':self._to
                    })