"""
Application configuration settings
"""
import os

class Config:
    """
    Common configurations
    """
    DEBUG = True
    SECRET_KEY = '\x1b\xa5*G\xca\x88@\xe37\x8e\x8cP\x18\xef\xa3\xc0r\xaa\xf4\x94H3\xc3\xfd'

class DevelopmentConfig(Config):
    """
    Development configurations
    """
    pass

class TestingConfig(Config):
    """
    Testing configurations
    """
    TESTING = True

class ProductionConfig(Config):
    """
    Production configurations
    """
    DEBUG = False

CONFIG = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
