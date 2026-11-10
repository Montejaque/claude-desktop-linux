#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
if ! python3 -c 'import tkinter' >/dev/null 2>&1; then
  echo "Falta Tkinter para Python 3. Instálalo mediante el soporte de software aprobado por tu organización." >&2
  exit 1
fi
PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}" python3 -m claude_installer.app
