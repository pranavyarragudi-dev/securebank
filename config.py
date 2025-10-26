import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'banking-secret-key-change-in-production'
    
    # --- Fix for Render PostgreSQL URLs ---
    # Render sometimes provides DATABASE_URL with "postgres://" prefix
    # SQLAlchemy requires "postgresql://"
    uri = os.environ.get('DATABASE_URL')  # Render or local env
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)

    # Database connection
    SQLALCHEMY_DATABASE_URI = uri or 'sqlite:///banking_app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # App settings
    WTF_CSRF_ENABLED = True
    
    # Transaction limits
    TRANSACTION_LIMIT_DAILY = float(os.environ.get('TXN_LIMIT_DAILY', '10000.00'))
    TRANSACTION_LIMIT_SINGLE = float(os.environ.get('TXN_LIMIT_SINGLE', '5000.00'))


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
