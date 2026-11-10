#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON:-python3}"
if ! "$PYTHON_BIN" -c 'import tkinter' >/dev/null 2>&1; then
  echo "No está disponible Tkinter para Python 3. En Ubuntu suele proporcionarlo python3-tk." >&2
  exit 1
fi
mkdir -p "$HOME/.local/bin"
cat > "$HOME/.local/bin/claude-desktop-installer" <<EOF
#!/usr/bin/env bash
ROOT="$ROOT"
PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}" exec "$PYTHON_BIN" -m claude_installer.app
EOF
chmod 700 "$HOME/.local/bin/claude-desktop-installer"
echo "Lanzador creado en ~/.local/bin/claude-desktop-installer"
