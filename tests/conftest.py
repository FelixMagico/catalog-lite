import threading

import pytest
from werkzeug.serving import make_server

from app import create_app
from app.extensions import db
from app.models import ROLE_ADMIN, Application, User


class TestConfig:
    SECRET_KEY = "test"
    SQLALCHEMY_DATABASE_URI = "sqlite://"  # database in memoria, MySQL non serve


def seed(app):
    """Un admin e due applicazioni di prova."""
    with app.app_context():
        db.create_all()
        admin = User(username="admin", role=ROLE_ADMIN)
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.add(Application(name="VLC", description="Lettore multimediale"))
        db.session.add(Application(name="7-Zip", description="Compressione file"))
        db.session.commit()


@pytest.fixture()
def client():
    """Client di test Flask (per i test dell'API)."""
    app = create_app(TestConfig)
    seed(app)
    return app.test_client()


@pytest.fixture(scope="session")
def base_url(tmp_path_factory):
    """Avvia il sito vero su una porta locale: serve a Playwright."""

    class LiveConfig(TestConfig):
        # file temporaneo: il server gira in un altro thread
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + str(tmp_path_factory.mktemp("db") / "test.db")

    app = create_app(LiveConfig)
    seed(app)
    server = make_server("127.0.0.1", 5055, app)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield "http://127.0.0.1:5055"
    server.shutdown()
