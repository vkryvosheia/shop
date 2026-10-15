# shop

A learning project: a test e-commerce platform, built one ticket at a time the
way a real team works. Work is tracked on the
[project board](https://github.com/users/vkryvosheia/projects/1). See
[CONTRIBUTING.md](CONTRIBUTING.md) for how to pick up a ticket and open a PR.

| Part     | Stack                                                      |
| -------- | ---------------------------------------------------------- |
| Backend  | Python 3.12, FastAPI, SQLAlchemy 2, Alembic, MySQL 8, pytest |
| Frontend | React, TypeScript, Vite, React Router, Vitest              |
| Tooling  | uv, ruff, ESLint, Prettier, Docker Compose, GitHub Actions |

```
backend/     FastAPI app (app/), migrations (migrations/), tests (tests/)
frontend/    React app (src/)
docker/      Files used by docker-compose.yml
.github/     CI workflow, issue and PR templates
```

## Prerequisites

Install these once:

- [Git](https://git-scm.com/downloads)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (runs MySQL for you). Start it before step 2.
- [uv](https://docs.astral.sh/uv/getting-started/installation/), the Python package manager. You don't need to install Python yourself: uv downloads Python 3.12 when needed.
- [Node.js 24 LTS](https://nodejs.org/) or newer. npm comes with it.

Check that everything is there:

```bash
git --version && docker --version && uv --version && node --version
```

The commands below are for macOS/Linux. On Windows, use Git Bash (installed with Git) and they work the same.

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/vkryvosheia/shop.git
cd shop
```

### 2. Start the database

From the repo root:

```bash
docker compose up -d --wait
```

This starts MySQL in the background and waits until it's ready (the first run downloads the image, so give it a minute). It creates two databases: `shop` for development and `shop_test` for the tests. Data is kept between restarts.

### 3. Run the backend

In a terminal, from the repo root:

```bash
cd backend
cp .env.example .env
uv sync
uv run alembic upgrade head
uv run uvicorn app.main:create_app --factory --reload
```

- `.env` holds your local settings. The defaults already match the database from step 2.
- `uv sync` creates `backend/.venv` and installs the dependencies.
- `alembic upgrade head` applies the database migrations.

The API runs at http://127.0.0.1:8000, and the interactive API docs are at http://127.0.0.1:8000/docs. There are no endpoints yet, so the docs page is empty. `--reload` restarts the server whenever you save a file. Stop it with `Ctrl+C`.

### 4. Run the frontend

In a **second** terminal, from the repo root:

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173. You should see a page that says "Shop".

In development, requests from the frontend to `/api/...` are forwarded to the backend on port 8000, so keep the backend running too.

## Running tests and checks

CI runs exactly these on every pull request. Run them before you push.

Backend (from `backend/`, database must be running):

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

`uv run ruff check --fix .` and `uv run ruff format .` fix most problems for you.

Frontend (from `frontend/`):

```bash
npm run test:run
npm run lint
npm run format:check
npm run typecheck
npm run build
```

`npm run format` fixes formatting. `npm test` runs the tests in watch mode while you work.

The backend tests use the `shop_test` database. It is wiped and rebuilt from the migrations on every test run, so don't keep anything there.

## Everyday commands

| What                          | Command (directory)                                       |
| ----------------------------- | --------------------------------------------------------- |
| Stop the database             | `docker compose down` (root)                              |
| Start it again                | `docker compose up -d --wait` (root)                      |
| Delete all database data      | `docker compose down -v` (root), then start it again      |
| Install new dependencies after a `git pull` | `uv sync` (backend), `npm install` (frontend) |
| Apply new migrations          | `uv run alembic upgrade head` (backend)                   |
| Create a migration            | `uv run alembic revision --autogenerate -m "add products table"` (backend) |
| Undo the last migration       | `uv run alembic downgrade -1` (backend)                   |
| Add a Python package          | `uv add <package>` (backend)                              |
| Add an npm package            | `npm install <package>` (frontend)                        |

## Troubleshooting

- **`database_url` … `Field required`**: the backend can't find its settings. Run `cp .env.example .env` inside `backend/`.
- **`Can't connect to MySQL server`**: the database isn't running. Start Docker Desktop, then `docker compose up -d --wait`.
- **`port is already allocated` / `address already in use` on 3306**: another MySQL is already running on your computer. Stop it, or change the left side of `"3306:3306"` in `docker-compose.yml` and the port in `backend/.env` to match.
- **`Access denied ... to database 'shop_test'`**: the database volume was created before the test database was added. Reset it with `docker compose down -v` and start it again. This deletes local data.
- **Frontend shows a proxy error, or requests to `/api` fail**: the backend isn't running on port 8000.
