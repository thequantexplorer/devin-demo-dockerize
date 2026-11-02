# Devin demo: Run an app in Docker with Postgres and Redis

**What it shows:** Devin writes a multi-stage Dockerfile and a docker-compose.yml for a Flask app, starts the stack, runs the migrations and tests inside it, proves the health endpoint works, and opens a pull request.

**Needs:** GitHub only

## Set it up

1. Click **Use this template → Create a new repository**, choose your GitHub account as the owner, and keep the name `devin-demo-dockerize`. The prompt below assumes that name. Use the template rather than a fork: pull requests on a fork go to the original repo by default.
2. In Devin, open [**Settings → Connections → GitHub**](https://app.devin.ai/settings/connections/github) and make sure Devin can access the new repository.
3. Optional: see the problem for yourself. In your copy on GitHub, click **Actions**, then **Stack check**, then **Run workflow**, then the green **Run workflow** button. The run fails because there is no `Dockerfile` or `docker-compose.yml`.

## Prompt

Start a new Devin session at [app.devin.ai](https://app.devin.ai) and paste this. Replace `<you>` with your GitHub user.

```text
The Flask app in https://github.com/<you>/devin-demo-dockerize needs Postgres and Redis, but it has no Docker setup. Read the README first.

1. Run the tests as they are and show me that they fail without Postgres and Redis.
2. Write a multi-stage Dockerfile: a build stage that installs the Python packages, and a small runtime stage that runs as a non-root user and serves the app with gunicorn on port 8000. The tests must be able to run inside the web container.
3. Write a docker-compose.yml with three services: web, postgres and redis. Give each one a health check, so `docker compose up -d --build --wait` only finishes when all three are healthy. Keep Postgres data in a named volume.
4. Start the stack. Run the migrations and the tests inside the web container, using the exact commands in the README section "What done looks like". Then call /health with curl and show the response.
5. Do not change the app code or the tests unless you have to. If you do, explain why.
6. Open a pull request. In the description, paste the output of each command from step 4 and the size of the final image. Make sure the Stack check workflow passes on the pull request.
```

## What to watch

- It shows the failing tests before it writes any Docker files.
- It waits for the health checks instead of guessing with `sleep`.
- It runs the migrations and tests inside the container, not on its own machine.

## You're done when

- Your copy has a pull request with a `Dockerfile` and a `docker-compose.yml`.
- The pull request description shows the migrations, a green test run, and `{"postgres":"ok","redis":"ok","status":"ok"}` from `/health`.
- The **Stack check** workflow has a green check on the pull request.
