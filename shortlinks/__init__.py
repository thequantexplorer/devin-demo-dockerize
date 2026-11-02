import os

from flask import Flask

from .extensions import db, migrate, redis_client


def create_app(config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "postgresql+psycopg://shortlinks:shortlinks@localhost:5432/shortlinks"
    )
    app.config["REDIS_URL"] = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    if config:
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)
    redis_client.init_app(app)

    from . import models  # noqa: F401
    from .routes import bp

    app.register_blueprint(bp)
    return app
