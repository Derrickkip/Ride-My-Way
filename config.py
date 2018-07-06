"""
Application configuration settings
"""
import os

class Config:
    """
    Common configurations
    """
    DEBUG = True
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

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
    DATABASE = os.getenv('TEST_DB')

class ProductionConfig(Config):
    """
    Production configurations
    """
    DEBUG = False
    DATABASE = os.getenv('PROD_DATABASE')

CONFIG = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
