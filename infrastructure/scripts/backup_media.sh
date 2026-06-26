#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
MEDIA_DIR="${MEDIA_DIR:-$ROOT_DIR/storage/media}"
BACKUP_DIR="${BACKUP_DIR:-$ROOT_DIR/backups/media}"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP_FILE="$BACKUP_DIR/media_${TIMESTAMP}.tar.gz"

mkdir -p "$BACKUP_DIR"

if [[ ! -d "$MEDIA_DIR" ]]; then
    printf "Media directory not found, creating empty directory: %s\n" "$MEDIA_DIR"
    mkdir -p "$MEDIA_DIR"
fi

tar -czf "$BACKUP_FILE" -C "$MEDIA_DIR" .

printf "Media backup created: %s\n" "$BACKUP_FILE"
