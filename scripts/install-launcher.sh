#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON:-python3}"
if ! "$PYTHON_BIN" -c 'import tkinter' >/dev/null 2>&1; then
  echo "No está disponible Tkinter para Python 3. En Ubuntu suele proporcionarlo python3-tk." >&2
  exit 1
fi
mkdir -p "$HOME/.local/bin" "$HOME/.local/share/applications"
cat > "$HOME/.local/bin/claude-desktop-installer" <<EOF
#!/usr/bin/env bash
ROOT="$ROOT"
PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}" exec "$PYTHON_BIN" -m claude_installer.app
EOF
chmod 700 "$HOME/.local/bin/claude-desktop-installer"
cat > "$HOME/.local/share/applications/claude-desktop-installer.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=Instalador de Claude Desktop
Comment=Instalar y actualizar Claude Desktop para este usuario
Exec="$HOME/.local/bin/claude-desktop-installer"
Icon=system-software-install
Terminal=false
Categories=Utility;System;
StartupNotify=true
EOF
chmod 644 "$HOME/.local/share/applications/claude-desktop-installer.desktop"
echo "Instalador añadido al menú de aplicaciones."
echo "Comando: ~/.local/bin/claude-desktop-installer"
