#!/usr/bin/env bash
#
# Script: osbgraph-start.sh
# Author: ObsGraph Team <dev@obsgraph.local>
# Created: 2026-03-16
#
# Purpose:
#   Start the ObsGraph-Flask application with Gunicorn from the pre-created
#   production virtual environment.
#
# Usage:
#   ./bin/osbgraph-start.sh [gunicorn-args]
#
# Examples:
#   ./bin/osbgraph-start.sh
#   ./bin/osbgraph-start.sh --workers 4
#

set -euo pipefail
IFS=$'\n\t'

readonly OBSGRAPH_PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
readonly OBSGRAPH_VENV_PATH="$OBSGRAPH_PROJECT_ROOT/.venv-prod"
readonly OBSGRAPH_GUNICORN_BIN="$OBSGRAPH_VENV_PATH/bin/gunicorn"
readonly OBSGRAPH_GUNICORN_CONF="$OBSGRAPH_PROJECT_ROOT/gunicorn.conf.py"
readonly OBSGRAPH_WSGI_APP="obsgraph_flask.wsgi:app"

if [[ ! -d "$OBSGRAPH_VENV_PATH" ]]; then
  echo "Error: Virtual environment not found: $OBSGRAPH_VENV_PATH" >&2
  echo "Run ./bin/osbgraph-config.sh first to create the production environment." >&2
  exit 1
fi

if [[ ! -x "$OBSGRAPH_GUNICORN_BIN" ]]; then
  echo "Error: gunicorn executable not found: $OBSGRAPH_GUNICORN_BIN" >&2
  echo "Install runtime dependencies in $OBSGRAPH_VENV_PATH before starting the application." >&2
  exit 1
fi

cd "$OBSGRAPH_PROJECT_ROOT"
source "$OBSGRAPH_VENV_PATH/bin/activate"

exec "$OBSGRAPH_GUNICORN_BIN" \
  --config "$OBSGRAPH_GUNICORN_CONF" \
  "$OBSGRAPH_WSGI_APP" \
  "$@"
