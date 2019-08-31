import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PRIVATE_KEY = os.environ.get('PRIVATE_KEY')
    TOKEN_EXPIRATION = os.environ.get('TOKEN_EXPIRATION')
    REQUIRE_AUTH_TOKEN = True


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///dev.db'
    TESTING = True
    TEMPLATES_AUTO_RELOAD = True
    REQUIRE_AUTH_TOKEN = False

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///test.db'
    TESTING = True
    TOKEN_EXPIRATION = 1
    REQUIRE_AUTH_TOKEN = False


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URL')


config = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig,
    'default': DevConfig
}
