import redis
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


class RedisClient:
    def __init__(self):
        self._client = None

    def init_app(self, app):
        self._client = redis.Redis.from_url(
            app.config["REDIS_URL"], socket_connect_timeout=2, decode_responses=True
        )

    def __getattr__(self, name):
        return getattr(self._client, name)


redis_client = RedisClient()
