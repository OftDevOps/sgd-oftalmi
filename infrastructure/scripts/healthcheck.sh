#!/usr/bin/env bash
set -euo pipefail

HEALTHCHECK_TIMEOUT="${HEALTHCHECK_TIMEOUT:-5}"

if [[ -n "${HEALTHCHECK_URL:-}" ]]; then
    curl --fail --silent --show-error --max-time "$HEALTHCHECK_TIMEOUT" "$HEALTHCHECK_URL"
    printf "\n"
    exit 0
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

cd "$ROOT_DIR"

docker compose exec -T backend python -c "from urllib.request import urlopen; response = urlopen('http://127.0.0.1:8000/health/', timeout=${HEALTHCHECK_TIMEOUT}); print(response.status, response.read().decode())"
