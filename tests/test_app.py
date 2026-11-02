def test_health_reports_postgres_and_redis(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok", "postgres": "ok", "redis": "ok"}


def test_create_and_follow_link_counts_clicks(client):
    resp = client.post("/links", json={"url": "https://devin.ai"})
    assert resp.status_code == 201
    code = resp.get_json()["code"]

    for _ in range(3):
        follow = client.get(f"/{code}")
        assert follow.status_code == 302
        assert follow.headers["Location"] == "https://devin.ai"

    stats = client.get(f"/links/{code}").get_json()
    assert stats["url"] == "https://devin.ai"
    assert stats["clicks"] == 3


def test_rejects_non_http_urls(client):
    resp = client.post("/links", json={"url": "javascript:alert(1)"})
    assert resp.status_code == 400


def test_unknown_code_is_404(client):
    assert client.get("/nope123").status_code == 404
    assert client.get("/links/nope123").status_code == 404
