import secrets
from urllib.parse import urlparse

from flask import Blueprint, abort, jsonify, redirect, request
from sqlalchemy import text

from .extensions import db, redis_client
from .models import Link

bp = Blueprint("shortlinks", __name__)


def _clicks_key(code):
    return f"clicks:{code}"


@bp.get("/health")
def health():
    checks = {}
    try:
        db.session.execute(text("SELECT 1"))
        checks["postgres"] = "ok"
    except Exception as exc:  # noqa: BLE001
        checks["postgres"] = f"error: {exc.__class__.__name__}"
    try:
        redis_client.ping()
        checks["redis"] = "ok"
    except Exception as exc:  # noqa: BLE001
        checks["redis"] = f"error: {exc.__class__.__name__}"
    healthy = all(v == "ok" for v in checks.values())
    return jsonify(status="ok" if healthy else "error", **checks), 200 if healthy else 503


@bp.post("/links")
def create_link():
    data = request.get_json(silent=True) or {}
    url = data.get("url", "")
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        return jsonify(error="url must be an http(s) URL"), 400
    link = Link(code=secrets.token_urlsafe(5), url=url)
    db.session.add(link)
    db.session.commit()
    return jsonify(link.to_dict()), 201


@bp.get("/links/<code>")
def link_stats(code):
    link = Link.query.filter_by(code=code).first()
    if link is None:
        abort(404)
    clicks = int(redis_client.get(_clicks_key(code)) or 0)
    return jsonify(link.to_dict(clicks=clicks))


@bp.get("/<code>")
def follow(code):
    link = Link.query.filter_by(code=code).first()
    if link is None:
        abort(404)
    redis_client.incr(_clicks_key(code))
    return redirect(link.url, code=302)
