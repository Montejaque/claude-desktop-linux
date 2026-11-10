#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
python3 -c 'import tkinter' >/dev/null 2>&1 || { echo "Falta Tkinter." >&2; exit 1; }
PYTHONPATH="$ROOT" exec python3 -m claude_installer.app
