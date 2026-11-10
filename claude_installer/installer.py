"""Per-user install, launch and uninstall operations for the community AppImage."""
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

from .release_source import ReleaseAsset, download_verified, get_latest_asset

APP_ID = "claude-desktop-unofficial"
APP_NAME = "Claude Desktop (versión comunitaria)"
INSTALL_DIR = Path.home() / ".local" / "opt" / APP_ID
APPLICATIONS_DIR = Path.home() / ".local" / "share" / "applications"
DESKTOP_FILE = APPLICATIONS_DIR / (APP_ID + ".desktop")
ICON_DIR = Path.home() / ".local" / "share" / "icons" / "hicolor" / "256x256" / "apps"
ICON_FILE = ICON_DIR / (APP_ID + ".png")


class InstallError(RuntimeError):
    pass


def is_installed() -> bool:
    return (INSTALL_DIR / "AppRun").is_file() and DESKTOP_FILE.is_file()


def installed_version() -> Optional[str]:
    version_file = INSTALL_DIR / "INSTALLER_VERSION"
    try:
        return version_file.read_text(encoding="utf-8").strip()
    except OSError:
        return None


def _copy_icon(extracted: Path) -> None:
    candidates = []
    for path in extracted.rglob("*"):
        if path.is_file() and path.suffix.lower() in (".png", ".svg"):
            low = path.name.lower()
            if "claude" in low or "icon" in low:
                candidates.append(path)
    pngs = [p for p in candidates if p.suffix.lower() == ".png"]
    if pngs:
        ICON_DIR.mkdir(parents=True, exist_ok=True)
        # Prefer the largest hicolor icon where a size is encoded in the path.
        selected = sorted(pngs, key=lambda p: (("256x256" in str(p)), p.stat().st_size))[-1]
        shutil.copy2(selected, ICON_FILE)
    else:
        raise InstallError("El paquete no contiene un icono PNG de Claude reconocible; no se ha creado el lanzador.")


def _write_desktop_file() -> None:
    APPLICATIONS_DIR.mkdir(parents=True, exist_ok=True)
    app_run = INSTALL_DIR / "AppRun"
    content = """[Desktop Entry]
Type=Application
Name=Claude Desktop (versión comunitaria)
Comment=Aplicación de escritorio de Claude — paquete comunitario no oficial
Exec="{app_run}"
Path="{workdir}"
Icon={icon}
Terminal=false
Categories=Office;Utility;
StartupNotify=true
""".format(app_run=app_run, workdir=INSTALL_DIR, icon=APP_ID)
    temporary = DESKTOP_FILE.with_suffix(".desktop.tmp")
    temporary.write_text(content, encoding="utf-8")
    temporary.chmod(0o644)
    temporary.replace(DESKTOP_FILE)


def install_latest(progress=None, status=None) -> str:
    asset = get_latest_asset()
    if status:
        status("Versión detectada: %s. Descargando y verificando SHA-256…" % asset.version)

    cache_dir = Path.home() / ".cache" / APP_ID
    package = cache_dir / asset.name
    download_verified(asset, package, progress=progress)

    if status:
        status("Integridad verificada. Extrayendo la aplicación…")

    INSTALL_DIR.parent.mkdir(parents=True, exist_ok=True)
    stage_parent = INSTALL_DIR.parent
    staging = Path(tempfile.mkdtemp(prefix=".claude-stage-", dir=str(stage_parent)))
    try:
        result = subprocess.run(
            [str(package), "--appimage-extract"],
            cwd=str(staging),
            env=dict(os.environ, APPIMAGE_EXTRACT_AND_RUN="1"),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=240,
        )
        extracted = staging / "squashfs-root"
        if result.returncode != 0 or not (extracted / "AppRun").is_file():
            tail = (result.stdout or "")[-1800:]
            raise InstallError("No se pudo extraer el AppImage. %s" % tail)

        backup = INSTALL_DIR.with_name(INSTALL_DIR.name + ".previous")
        if backup.exists():
            shutil.rmtree(backup)
        if INSTALL_DIR.exists():
            INSTALL_DIR.rename(backup)
        try:
            shutil.copytree(extracted, INSTALL_DIR, symlinks=True)
            (INSTALL_DIR / "INSTALLER_VERSION").write_text(asset.version + "\n", encoding="utf-8")
            _copy_icon(INSTALL_DIR)
            _write_desktop_file()
        except Exception:
            if INSTALL_DIR.exists():
                shutil.rmtree(INSTALL_DIR)
            if backup.exists():
                backup.rename(INSTALL_DIR)
            raise
        if backup.exists():
            shutil.rmtree(backup)
        return asset.version
    finally:
        shutil.rmtree(staging, ignore_errors=True)


def launch() -> None:
    app_run = INSTALL_DIR / "AppRun"
    if not app_run.is_file():
        raise InstallError("Claude Desktop no está instalado.")
    env = os.environ.copy()
    env.setdefault("ELECTRON_DISABLE_SECURITY_WARNINGS", "true")
    subprocess.Popen([str(app_run)], cwd=str(INSTALL_DIR), env=env, start_new_session=True)


def uninstall() -> None:
    if INSTALL_DIR.exists():
        shutil.rmtree(INSTALL_DIR)
    for path in (DESKTOP_FILE, ICON_FILE):
        try:
            path.unlink()
        except FileNotFoundError:
            pass
    for directory in (ICON_DIR, ICON_DIR.parent, ICON_DIR.parent.parent):
        try:
            directory.rmdir()
        except OSError:
            pass
