import pytest
from sqlalchemy import text

from shortlinks import create_app
from shortlinks.extensions import db, redis_client


@pytest.fixture()
def app():
    app = create_app({"TESTING": True})
    with app.app_context():
        db.session.execute(text("TRUNCATE links RESTART IDENTITY"))
        db.session.commit()
        redis_client.flushdb()
        yield app
        db.session.remove()


@pytest.fixture()
def client(app):
    return app.test_client()
