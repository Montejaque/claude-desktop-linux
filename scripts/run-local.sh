#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
if ! python3 -c 'import tkinter' >/dev/null 2>&1; then
  echo "Falta Tkinter para Python 3. En Ubuntu suele instalarse como python3-tk." >&2
  exit 1
fi
PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}" exec python3 -m claude_installer.app
