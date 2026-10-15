#!/usr/bin/env bash
# Start the backend for local development, in one go:
#   database container up -> backend/.env present -> migrations applied -> API with auto-reload.
#
# Usage (works from any directory):
#   backend/scripts/dev.sh                 # http://127.0.0.1:8000
#   backend/scripts/dev.sh --port 8001     # extra options are passed to uvicorn
set -euo pipefail

BACKEND_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_DIR="$(dirname "$BACKEND_DIR")"

if ! docker info >/dev/null 2>&1; then
  echo "Docker isn't running. Start Docker Desktop and try again." >&2
  exit 1
fi

echo "==> Starting the database (if it isn't running yet)"
docker compose -f "$REPO_DIR/docker-compose.yml" up -d --wait db

cd "$BACKEND_DIR"

if [[ ! -f .env ]]; then
  echo "==> Creating backend/.env from .env.example"
  cp .env.example .env
fi

echo "==> Applying database migrations"
uv run alembic upgrade head

echo "==> Starting the API (docs at /docs, stop with Ctrl+C)"
exec uv run uvicorn app.main:create_app --factory --reload "$@"
