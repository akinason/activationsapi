import os
import json
import configparser
from activationsapi import BASE_DIR

config = configparser.ConfigParser()
config.read(os.path.join(BASE_DIR, 'config.ini'))

DEBUG = json.loads(str(config.get('base', 'DEBUG')).lower())


class Base:
    BASE_DIR = BASE_DIR
    DEBUG = True
    SECRET_KEY = config.get('base', 'SECRET_KEY')
    DBNAME = config.get('database', 'DBNAME')
    DBUSER = config.get('database', 'DBUSER')
    DBPASSWORD = config.get('database', 'DBPASSWORD')
    AWS_ACCESS_KEY_ID = config.get("spaces", "AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = config.get("spaces", "AWS_SECRET_ACCESS_KEY")

    DEFAULT_FROM_EMAIL = config.get('mail', 'DEFAULT_FROM_EMAIL')
    DEFAULT_FROM_NAME = config.get('mail', 'DEFAULT_FROM_NAME')
    MAIL_SERVER = config.get('mail', 'EMAIL_HOST')
    MAIL_PORT = config.get('mail', 'EMAIL_PORT')
    MAIL_USE_TLS = json.loads(str(config.get('mail', 'EMAIL_USE_TLS')).lower())  # Convert to python boolean
    MAIL_USERNAME = config.get('mail', 'EMAIL_HOST_USER')
    MAIL_PASSWORD = config.get('mail', 'EMAIL_HOST_PASSWORD')
    GLOXON_APP_ID = config.get('oauth', 'GLOXON_APP_ID')
    GLOXON_APP_KEY = config.get('oauth', 'GLOXON_APP_KEY')
    GLOXON_APP_SECRET = config.get('oauth', 'GLOXON_APP_SECRET')

class Development(Base):
    ALLOWED_HOSTS = config.get('base', 'ALLOWED_HOSTS').split(',')
    STATIC_ROOT = "/var/www/html/activationsapi/static/"
    STATIC_URL = '/static/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'


class Production(Base):
    DEBUG = False
    ALLOWED_HOSTS = config.get('base', 'ALLOWED_HOSTS').split(',')
    STATIC_ROOT = "/var/www/html/activationsapi/static/"
    STATIC_URL = '/static/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'


configuration = Development() if DEBUG else Production()

