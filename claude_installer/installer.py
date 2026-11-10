"""Official Anthropic Claude Desktop per-user installation."""
from __future__ import annotations
import os,shutil,subprocess,tempfile
from pathlib import Path
from .release_source import ReleaseError,download_verified,get_latest_package
APP_ID="claude-desktop"
INSTALL_DIR=Path.home()/".local/opt"/APP_ID
WRAPPER=Path.home()/".local/bin/claude-desktop-oficial"
APPLICATIONS=Path.home()/".local/share/applications"
DESKTOP=APPLICATIONS/"claude-desktop.desktop"
ICON_DIR=Path.home()/".local/share/icons/hicolor/256x256/apps"
ICON=ICON_DIR/"claude-desktop.png"
CACHE=Path.home()/".cache/claude-desktop-installer"
class InstallError(RuntimeError): pass
def is_installed(): return (INSTALL_DIR/"usr/lib/claude-desktop/claude-desktop").is_file()
def installed_version():
    try: return (INSTALL_DIR/"INSTALLER_VERSION").read_text(encoding="utf-8").strip()
    except OSError: return None
def version_is_newer(candidate, current):
    """Compare Debian package versions; return None if comparison is unavailable."""
    if not candidate or not current or not shutil.which("dpkg"):
        return None
    result = subprocess.run(
        ["dpkg", "--compare-versions", str(candidate), "gt", str(current)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False,
    )
    return result.returncode == 0

def _optional(command):
    try: subprocess.run(command,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=15,check=False)
    except (OSError,subprocess.SubprocessError): pass
def repair_access():
    if not is_installed(): raise InstallError("Claude Desktop no está instalado.")
    WRAPPER.parent.mkdir(parents=True,exist_ok=True)
    content='''#!/bin/sh
APP="$HOME/.local/opt/claude-desktop/usr/lib/claude-desktop"
export LD_LIBRARY_PATH="$APP"
exec "$APP/claude-desktop" "$@"
'''
    temp=WRAPPER.with_suffix(".tmp"); temp.write_text(content,encoding="utf-8"); temp.chmod(0o700); temp.replace(WRAPPER)
    source=INSTALL_DIR/"usr/share/icons/hicolor/256x256/apps/claude-desktop.png"
    if not source.is_file(): source=INSTALL_DIR/"usr/share/icons/hicolor/128x128/apps/claude-desktop.png"
    if source.is_file(): ICON_DIR.mkdir(parents=True,exist_ok=True); shutil.copy2(source,ICON)
    APPLICATIONS.mkdir(parents=True,exist_ok=True)
    desktop="""[Desktop Entry]
Version=1.0
Type=Application
Name=Claude
Comment=Claude Desktop oficial de Anthropic
Exec={wrapper} %U
Icon=claude-desktop
Terminal=false
Categories=Office;Utility;Development;
StartupNotify=true
StartupWMClass=com.anthropic.Claude
MimeType=x-scheme-handler/claude;
""".format(wrapper=WRAPPER)
    temp=DESKTOP.with_suffix(".desktop.tmp"); temp.write_text(desktop,encoding="utf-8"); temp.chmod(0o644); temp.replace(DESKTOP)
    _optional(["update-desktop-database",str(APPLICATIONS)])
    _optional(["xdg-mime","default",DESKTOP.name,"x-scheme-handler/claude"])
def install_latest(progress=None,status=None):
    if not shutil.which("dpkg-deb"): raise InstallError("Falta dpkg-deb. No se ha modificado el sistema.")
    with tempfile.TemporaryDirectory(prefix="claude-verify-") as temp:
        try: package=get_latest_package(Path(temp),status=status)
        except ReleaseError as exc: raise InstallError(str(exc))
    if status: status("Versión oficial %s detectada. Descargando y verificando…"%package.version)
    archive=CACHE/("claude-desktop_%s_%s.deb"%(package.version,package.architecture))
    try: download_verified(package,archive,progress)
    except ReleaseError as exc: raise InstallError(str(exc))
    parent=INSTALL_DIR.parent; parent.mkdir(parents=True,exist_ok=True)
    staging=Path(tempfile.mkdtemp(prefix=".claude-stage-",dir=str(parent))); extracted=staging/"package"; extracted.mkdir()
    try:
        if status: status("SHA-256 correcto. Extrayendo paquete oficial…")
        result=subprocess.run(["dpkg-deb","-x",str(archive),str(extracted)],capture_output=True,text=True,timeout=180)
        if result.returncode or not (extracted/"usr/lib/claude-desktop/claude-desktop").is_file():
            raise InstallError("No se pudo extraer el paquete: "+(result.stderr or "")[-1000:])
        (extracted/"INSTALLER_VERSION").write_text(package.version+"\n",encoding="utf-8")
        backup=INSTALL_DIR.with_name(INSTALL_DIR.name+".previous")
        if backup.exists(): shutil.rmtree(backup)
        if INSTALL_DIR.exists(): INSTALL_DIR.rename(backup)
        try:
            extracted.rename(INSTALL_DIR); repair_access()
        except Exception:
            if INSTALL_DIR.exists(): shutil.rmtree(INSTALL_DIR)
            if backup.exists(): backup.rename(INSTALL_DIR); repair_access()
            raise
        if backup.exists(): shutil.rmtree(backup)
        return package.version
    finally: shutil.rmtree(staging,ignore_errors=True)
def check_latest(status=None):
    with tempfile.TemporaryDirectory(prefix="claude-check-") as temp: return get_latest_package(Path(temp),status=status)
def launch():
    if not is_installed(): raise InstallError("Claude Desktop no está instalado.")
    repair_access()
    subprocess.Popen([str(WRAPPER)],cwd=str(INSTALL_DIR),env=os.environ.copy(),stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,start_new_session=True)
def uninstall():
    if INSTALL_DIR.exists(): shutil.rmtree(INSTALL_DIR)
    if CACHE.exists(): shutil.rmtree(CACHE)
    for path in (DESKTOP,WRAPPER,ICON):
        try: path.unlink()
        except FileNotFoundError: pass
    _optional(["update-desktop-database",str(APPLICATIONS)])
