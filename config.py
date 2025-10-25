import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'banking-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///banking_app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    TRANSACTION_LIMIT_DAILY = float(os.environ.get('TXN_LIMIT_DAILY', '10000.00'))
    TRANSACTION_LIMIT_SINGLE = float(os.environ.get('TXN_LIMIT_SINGLE', '5000.00'))

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
