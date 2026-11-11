#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
APPIMAGETOOL="$ROOT/.tools/appimagetool"
rm -rf build dist AppDir
if [[ "${PYINSTALLER_BUILD_IN_FOCAL:-0}" == "1" ]]; then
  command -v docker >/dev/null || { echo "ERROR: Docker no está disponible en el runner" >&2; exit 1; }
  docker run --rm -v "$ROOT:/src" -w /src ubuntu:20.04 bash -lc '
    set -euo pipefail
    export DEBIAN_FRONTEND=noninteractive
    apt-get update
    apt-get install -y --no-install-recommends python3 python3-tk python3-dev python3-pip python3.8-dev binutils patchelf
    python3 -m pip install --upgrade "pip<25"
    python3 -m pip install "pyinstaller==6.11.1"
    python3 -m PyInstaller --noconfirm --clean --onedir --windowed --name claude-desktop-installer --collect-all tkinter --hidden-import _tkinter --add-data "docs/GUIA_USUARIO.md:docs" launcher.py
    LIBPYTHON="$(find dist/claude-desktop-installer -maxdepth 2 -name "libpython3*.so*" -print -quit)"
    test -n "$LIBPYTHON"
    MAX_GLIBC="$(readelf --version-info "$LIBPYTHON" | grep -Eo "GLIBC_[0-9.]+" | sort -Vu | tail -n1 | cut -d_ -f2)"
    echo "GLIBC máxima requerida por $LIBPYTHON: $MAX_GLIBC"
    dpkg --compare-versions "$MAX_GLIBC" le 2.31 || { echo "ERROR: el binario supera GLIBC 2.31" >&2; exit 1; }
  '
else
  command -v python3 >/dev/null
  python3 -c 'import tkinter'
  python3 -m PyInstaller --version >/dev/null
  python3 -m PyInstaller --noconfirm --clean --onedir --windowed --name claude-desktop-installer --collect-all tkinter --hidden-import _tkinter --add-data "docs/GUIA_USUARIO.md:docs" launcher.py
fi
rm -rf AppDir
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
