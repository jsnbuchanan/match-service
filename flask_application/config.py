import logging
import os
from pymongo.uri_parser import parse_uri


class Config(object):
    def __init__(self):
        self.DEBUG = False
        self.TESTING = False
        self.HEROKU = False
        self.PRODUCTION = False

        self.SECRET_KEY = 'This is a secret key that no one will ever know'
        self.SITE_NAME = 'Flask Site'
        self.LOG_LEVEL = logging.DEBUG
        self.SERVER_NAME = 'localhost:5000'

        self.SYS_ADMINS = ['foo@example.com']

        # Mongodb support
        self.MONGODB_SETTINGS = self.mongo_from_uri(
            'mongodb://localhost:27017/development'
        )

        # Configured for Gmail
        self.DEFAULT_MAIL_SENDER = 'Jason <fitnessfocusball@gmail.com>'
        self.MAIL_SERVER = 'smtp.gmail.com'
        self.MAIL_PORT = 465
        self.MAIL_USE_SSL = True
        self.MAIL_USERNAME = 'fitnessfocusball@gmail.com'
        self.MAIL_PASSWORD = '4theworld'

        # Flask-Security setup
        self.SECURITY_EMAIL_SENDER = 'Security < security@example.com >'
        self.SECURITY_LOGIN_WITHOUT_CONFIRMATION = True
        self.SECURITY_REGISTERABLE = True
        self.SECURITY_RECOVERABLE = True
        self.SECURITY_URL_PREFIX = '/auth'
        self.SECUIRTY_POST_LOGIN = '/'
        self.SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
        # import uuid; salt = uuid.uuid4().hex
        self.SECURITY_PASSWORD_SALT = 'd3556e4eeeb4430fae0fa706ee7d8bdf'

        self.SECURITY_CONFIRMABLE = True
        self.SECURITY_LOGIN_WITHOUT_CONFIRMATION = False

        # CACHE
        self.CACHE_TYPE = 'simple'

    @staticmethod
    def mongo_from_uri(uri):
        config = parse_uri(uri)
        conn_settings = {
            'db': config['database'],
            'username': config['username'],
            'password': config['password'],
            'host': config['nodelist'][0][0],
            'port': config['nodelist'][0][1]
        }
        return conn_settings


class ProductionConfig(Config):
    def __init__(self):
        super(ProductionConfig, self).__init__()
        self.ENVIRONMENT = 'Production'
        self.HEROKU = True
        self.PRODUCTION = True
        self.LOG_LEVEL = logging.INFO
        self.SERVER_NAME = 'example.com'

        self.MAIL_SERVER = 'smtp.mandrillapp.com'
        self.MAIL_PORT = 587
        self.MAIL_USE_SSL = True
        self.MAIL_USERNAME = os.getenv('jsnbuchanan@gmail.com')
        self.MAIL_PASSWORD = os.getenv('yx4sFrcY1OtaQWDpLI3k1w')

        self.MONGODB_SETTINGS = self.mongo_from_uri(os.getenv('MONGOHQ_URL'))


class DevelopmentConfig(Config):
    '''
    Use "if app.debug" anywhere in your code,
    that code will run in development mode.
    '''
    def __init__(self):
        super(DevelopmentConfig, self).__init__()
        self.ENVIRONMENT = 'Dev'
        self.DEBUG = True
        self.TESTING = False


class TestingConfig(Config):
    '''
    A Config to use when we are running tests.
    '''
    def __init__(self):
        super(TestingConfig, self).__init__()
        self.ENVIRONMENT = 'Testing'
        self.DEBUG = False
        self.TESTING = True

        self.MONGODB_SETTINGS = self.mongo_from_uri(
            'mongodb://localhost:27017/testing'
        )


environment = os.getenv('ENVIRONMENT', 'DEVELELOPMENT').lower()
# Alternatively this may be easier if you are managing multiple aws servers:
# environment = socket.gethostname().lower()

if environment == 'testing':
    app_config = TestingConfig()
elif environment == 'production':
    app_config = ProductionConfig()
else:
    app_config = DevelopmentConfig()
