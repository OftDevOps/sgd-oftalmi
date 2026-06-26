#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

cd "$ROOT_DIR"

docker compose build backend
docker compose up -d db backend
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py check

printf "Backend deployment validation completed.\n"
