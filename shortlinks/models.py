from datetime import datetime, timezone

from .extensions import db


class Link(db.Model):
    __tablename__ = "links"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(16), unique=True, nullable=False, index=True)
    url = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self, clicks=0):
        return {
            "code": self.code,
            "url": self.url,
            "created_at": self.created_at.isoformat(),
            "clicks": clicks,
        }
