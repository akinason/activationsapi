import jinja2
import smtplib
import os
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from activationsapi import BASE_DIR
from config import configuration as conf

MAIL_DEFAULT_FROM = conf.DEFAULT_FROM_EMAIL
MAIL_SERVER = conf.MAIL_SERVER
MAIL_USERNAME = conf.MAIL_USERNAME
MAIL_PASSWORD = conf.MAIL_PASSWORD
MAIL_PORT = conf.MAIL_PORT
MAIL_USE_TLS = conf.MAIL_USE_TLS


def render_template(template_name, **kwargs):
    search_path = os.path.join(BASE_DIR, "templates/email")
    loader = jinja2.FileSystemLoader(searchpath=search_path)
    env = jinja2.Environment(loader=loader)
    template = env.get_template(template_name)
    return template.render(**kwargs)


class Message:

    def __init__(self, sender=None, recipients=None, subject=None, body=None, html=False):
        self.sender = sender if sender else MAIL_DEFAULT_FROM
        self.recipients = []
        if recipients:
            if type(recipients) == str:
                self.recipients.append(recipients)
            elif type(recipients) in [tuple, list]:
                self.recipients = [recipient for recipient in recipients]
        self.subject = subject
        self.body = body
        self.html = html

    def is_valid(self):
        """
        Just a basic check to ensure all required elements needed to send an email have been set.

        TODO: Define Explicit Exceptions for each attribute.
        """

        if not self.sender:
            raise Exception('Sender not set.')
        if not self.recipients or len(self.recipients) == 0:
            raise Exception('No recipients specified.')
        if not self.subject:
            raise Exception('Email must have a subject.')
        if not self.body and not self.html:
            raise Exception('Email must contain body or html.')
        return True

    def add_recipient(self, recipient):
        self.recipients.append(recipient)


message = Message()


class Mail:
    """
    Class used to send emails.
    """
    def __init__(self, msg=None):
        self.message = msg
        self._server = MAIL_SERVER
        self._port = MAIL_PORT
        self._username = MAIL_USERNAME
        self._password = MAIL_PASSWORD
        self._use_tls = MAIL_USE_TLS
        self._context = ssl.create_default_context()

    def send(self, msg=None):
        if msg:
            self.message = msg

        if not self.message:
            raise Exception('Please include the message to be sent.')

        if not isinstance(self.message, Message):
            raise Exception('message must be an instance of Message.')
        try:
            self.message.is_valid()
            pass
        except Exception:
            raise

        # message is clean and good for sending.
        return self._send_mail()

    def _send_mail(self):

        msg = MIMEMultipart('alternative')

        if self.message.body:
            part1 = MIMEText(self.message.body if self.message.body else '', 'plain')
            msg.attach(part1)
        if self.message.html:
            part2 = MIMEText(self.message.html, 'html')
            msg.attach(part2)

        msg['Subject'] = self.message.subject
        msg['From'] = self.message.sender

        server = smtplib.SMTP_SSL(host=self._server, port=self._port)
        server.login(self._username, self._password)

        for recipient in self.message.recipients:
            _msg = msg
            _msg['To'] = recipient
            _msg.as_string()
            server.sendmail(from_addr=self.message.sender, to_addrs=recipient, msg=_msg.as_string().encode('utf-8'))
        server.quit()

        return "Email sent."


mail = Mail()
