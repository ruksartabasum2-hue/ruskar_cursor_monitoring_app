import os

from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)

    # Demo fallback only; set SECRET_KEY in .env for anything beyond local demo.
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-change-me")
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

    from app.routes.main import bp as main_bp

    app.register_blueprint(main_bp)

    return app
