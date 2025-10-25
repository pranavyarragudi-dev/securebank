from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy import text, inspect
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Load environment-based config
    env = os.environ.get("FLASK_ENV", "production")
    if env == "development":
        from config import DevelopmentConfig as AppConfig
    else:
        from config import ProductionConfig as AppConfig
    app.config.from_object(AppConfig)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "info"

    # Health check endpoint (for monitoring)
    @app.route("/health")
    def health_check():
        try:
            db.session.execute(text("SELECT 1"))
            return jsonify({
                "status": "healthy",
                "database": "connected",
                "version": "1.0.0",
                "environment": env
            }), 200
        except Exception as e:
            return jsonify({
                "status": "unhealthy",
                "database": "disconnected",
                "error": str(e)
            }), 503

    # Readiness probe
    @app.route("/ready")
    def readiness_check():
        try:
            db.session.execute(text("SELECT 1"))
            return jsonify({
                "ready": True,
                "database": "operational"
            }), 200
        except Exception as e:
            return jsonify({
                "ready": False,
                "database": "unavailable",
                "error": str(e)
            }), 503

    # Register Blueprints
    from banking_app.auth import bp as auth_bp
    from banking_app.customer import bp as customer_bp
    from banking_app.admin import bp as admin_bp
    from banking_app.main import bp as main_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(customer_bp, url_prefix="/customer")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(main_bp)

    # Create tables only if they don’t exist
    with app.app_context():
        inspector = inspect(db.engine)
        existing_tables = inspector.get_table_names()
        if not existing_tables:
            db.create_all(checkfirst=True)

    return app


@login_manager.user_loader
def load_user(user_id):
    from banking_app.models import User
    return User.query.get(int(user_id))
