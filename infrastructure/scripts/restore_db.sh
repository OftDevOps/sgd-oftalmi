#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 || -z "${1:-}" ]]; then
    printf "Usage: %s path/to/backup.sql\n" "$0" >&2
    exit 1
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BACKUP_FILE="$1"

cd "$ROOT_DIR"

if [[ ! -f "$BACKUP_FILE" ]]; then
    printf "Backup file not found: %s\n" "$BACKUP_FILE" >&2
    exit 1
fi

if [[ -f .env ]]; then
    set -a
    # shellcheck disable=SC1091
    source .env
    set +a
fi

POSTGRES_DB="${POSTGRES_DB:-sgd_oftalmi}"
POSTGRES_USER="${POSTGRES_USER:-sgd_user}"

docker compose exec -T db psql \
    --username "$POSTGRES_USER" \
    --dbname "$POSTGRES_DB" \
    < "$BACKUP_FILE"

printf "Database restored from: %s\n" "$BACKUP_FILE"
