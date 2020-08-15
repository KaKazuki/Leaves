class BaseConfig(object):
    DEBUG = False
    TESTING = False


class ProductionConfig(BaseConfig):
    pass


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(BaseConfig):
    TESTING = True
