#!/bin/bash
# Thin wrapper: the real logic is in uninstall.py (no jq needed).
set -e
D="$(cd "$(dirname "$0")" && pwd)"
for p in python3 python py; do "$p" -c "import sys" >/dev/null 2>&1 && exec "$p" "$D/uninstall.py" "$@"; done
echo "no working Python found" >&2; exit 1
