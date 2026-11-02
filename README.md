# acme-shortlinks

A small link shortener built with Flask.

- `POST /links` with `{"url": "https://..."}` creates a short code.
- `GET /<code>` redirects to the URL and counts the click.
- `GET /links/<code>` shows the URL and its click count.
- `GET /health` checks Postgres and Redis.

Links are stored in **Postgres** (migrations in `migrations/`, run with Flask-Migrate).
Click counts are stored in **Redis**.

## Settings

| Variable | Default |
| --- | --- |
| `DATABASE_URL` | `postgresql+psycopg://shortlinks:shortlinks@localhost:5432/shortlinks` |
| `REDIS_URL` | `redis://localhost:6379/0` |

## The problem

There is no Docker setup yet. Every developer has to install Postgres and Redis by hand.
Without them, the tests cannot run:

```text
$ pip install -r requirements-dev.txt
$ python -m pytest -q
EEEE
...
E   sqlalchemy.exc.OperationalError: (psycopg.OperationalError) connection failed:
    connection to server at "127.0.0.1", port 5432 failed: Connection refused
...
4 errors in 0.99s
```

The **Stack check** workflow (`.github/workflows/stack-check.yml`) also fails, because there is no `Dockerfile` or `docker-compose.yml`.

## What "done" looks like

From a fresh clone, these commands work:

```sh
docker compose up -d --build --wait                  # web, postgres and redis; web on port 8000
docker compose exec -T web flask --app wsgi db upgrade
docker compose exec -T web python -m pytest -q
curl -fsS http://localhost:8000/health               # {"postgres":"ok","redis":"ok","status":"ok"}
```

The **Stack check** workflow runs the same commands on every pull request.

---

This repo is a starter for a Devin workshop lab. See [DEVIN_DEMO.md](DEVIN_DEMO.md) for the steps and the prompt.
