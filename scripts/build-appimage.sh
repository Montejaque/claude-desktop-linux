#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
APPIMAGETOOL="$ROOT/.tools/appimagetool"
command -v python3 >/dev/null
python3 -c 'import tkinter'
python3 -m PyInstaller --version >/dev/null
if [[ ! -x "$APPIMAGETOOL" ]]; then
 mkdir -p "$ROOT/.tools"
 curl -fL --retry 3 "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage" -o "$APPIMAGETOOL"
 chmod +x "$APPIMAGETOOL"
fi
rm -rf build dist AppDir
python3 -m PyInstaller --noconfirm --clean --onedir --windowed --name claude-desktop-installer --collect-all tkinter --hidden-import _tkinter --add-data "docs/GUIA_USUARIO.md:docs" launcher.py
mkdir -p AppDir/usr/bin AppDir/usr/share/applications AppDir/usr/share/icons/hicolor/scalable/apps dist
cp -a dist/claude-desktop-installer/. AppDir/usr/bin/
cp assets/claude-installer.svg AppDir/usr/share/icons/hicolor/scalable/apps/claude-desktop-installer.svg
test -x AppDir/usr/bin/claude-desktop-installer
cat > AppDir/AppRun <<'EOF'
#!/bin/sh
set -eu
HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
APP="$HERE/usr/bin/claude-desktop-installer"
if [ ! -x "$APP" ]; then
  echo "ERROR: no se encuentra el ejecutable: $APP" >&2
  echo "Contenido de $HERE/usr/bin:" >&2
  ls -la "$HERE/usr/bin" >&2
  exit 127
fi
exec "$APP" "$@"
EOF
chmod +x AppDir/AppRun
cat > AppDir/claude-desktop-installer.desktop <<'EOF'
[Desktop Entry]
Type=Application
Name=Claude Desktop Installer
Comment=Instalador oficial de Claude Desktop para Linux
Exec=AppRun
Icon=claude-desktop-installer
Terminal=false
Categories=Utility;System;
EOF
cp AppDir/claude-desktop-installer.desktop AppDir/usr/share/applications/
ln -sf usr/share/icons/hicolor/scalable/apps/claude-desktop-installer.svg AppDir/claude-desktop-installer.svg
APPIMAGE_EXTRACT_AND_RUN=1 "$APPIMAGETOOL" AppDir dist/Claude-Desktop-Installer-x86_64.AppImage
test -s dist/Claude-Desktop-Installer-x86_64.AppImage
file dist/Claude-Desktop-Installer-x86_64.AppImage
chmod +x dist/Claude-Desktop-Installer-x86_64.AppImage
echo "Creada dist/Claude-Desktop-Installer-x86_64.AppImage"
