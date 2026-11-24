from flask import Flask

from .config import Config
from .extensions import db, login_manager, migrate


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    if not app.config.get("SECRET_KEY") or not app.config.get("SQLALCHEMY_DATABASE_URI"):
        raise RuntimeError(
            "Mancano SECRET_KEY o DATABASE_URL: compila il file .env"
        )

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from . import models  # noqa: F401  (serve a Flask-Migrate per vedere le tabelle)
    from .admin import bp as admin_bp
    from .auth import bp as auth_bp
    from .main import bp as main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)

    from .cli import seed_db

    app.cli.add_command(seed_db)

    return app
