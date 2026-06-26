#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BACKUP_DIR="${BACKUP_DIR:-$ROOT_DIR/backups/database}"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"

cd "$ROOT_DIR"

if [[ -f .env ]]; then
    set -a
    # shellcheck disable=SC1091
    source .env
    set +a
fi

POSTGRES_DB="${POSTGRES_DB:-sgd_oftalmi}"
POSTGRES_USER="${POSTGRES_USER:-sgd_user}"
BACKUP_FILE="$BACKUP_DIR/${POSTGRES_DB}_${TIMESTAMP}.sql"

mkdir -p "$BACKUP_DIR"

docker compose exec -T db pg_dump \
    --username "$POSTGRES_USER" \
    --dbname "$POSTGRES_DB" \
    --format plain \
    --no-owner \
    --no-privileges \
    > "$BACKUP_FILE"

printf "Database backup created: %s\n" "$BACKUP_FILE"
