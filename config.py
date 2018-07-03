"""
Application configuration settings
"""
import os

class Config:
    """
    Common configurations
    """
    DEBUG = True
    JWT_SECRET_KEY = '\x1b\xa5*G\xca\x88@\xe37\x8e\x8cP\x18\xef\xa3\xc0r\xaa\xf4\x94H3\xc3\xfd'

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
    DATABASE = "postgresql://testuser:testuser@localhost/testdb"

class ProductionConfig(Config):
    """
    Production configurations
    """
    DEBUG = False
    DATABASE = 'postgres://oyouuwhharkdie:c784d1dc881d562d9720ab3cce810c1dd9bffc4b74f04adf9aa9ccd23946d5f1@ec2-79-125-127-60.eu-west-1.compute.amazonaws.com:5432/d2s6sniq4ne115'

CONFIG = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
