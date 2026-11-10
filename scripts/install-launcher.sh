#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$HOME/.local/bin" "$HOME/.local/share/applications"
cat > "$HOME/.local/bin/claude-desktop-installer" <<EOF
#!/usr/bin/env bash
cd "$ROOT"
PYTHONPATH="$ROOT" exec python3 -m claude_installer.app
EOF
chmod 700 "$HOME/.local/bin/claude-desktop-installer"
cat > "$HOME/.local/share/applications/claude-desktop-installer.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=Claude Desktop Installer
Comment=Instalar Claude Desktop oficial de Anthropic
Exec=$HOME/.local/bin/claude-desktop-installer
Icon=system-software-install
Terminal=false
Categories=Utility;System;
StartupNotify=true
EOF
chmod 644 "$HOME/.local/share/applications/claude-desktop-installer.desktop"
update-desktop-database "$HOME/.local/share/applications" 2>/dev/null || true
echo "Instalador añadido al menú de aplicaciones."
