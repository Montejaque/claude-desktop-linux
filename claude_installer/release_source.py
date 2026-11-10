"""Download and cryptographically verify the official Anthropic APT package."""
from __future__ import annotations
import hashlib, platform, re, shutil, subprocess, urllib.request
from dataclasses import dataclass
from pathlib import Path

BASE_URL="https://downloads.claude.ai/claude-desktop/apt/stable"
KEY_URL="https://downloads.claude.ai/claude-desktop/key.asc"
EXPECTED_FINGERPRINT="31DDDE24DDFAB679F42D7BD2BAA929FF1A7ECACE"
MAX_INDEX_BYTES=30*1024*1024
MAX_PACKAGE_BYTES=900*1024*1024
USER_AGENT="PuntoVuelaMontejaque-ClaudeDesktopInstaller/1.0.1"
class ReleaseError(RuntimeError): pass
@dataclass(frozen=True)
class PackageInfo:
    version:str
    architecture:str
    filename:str
    sha256:str
    size:int
    url:str

def _request(url,timeout=45):
    return urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":USER_AGENT}),timeout=timeout)
def architecture():
    machine=platform.machine().lower()
    if machine in ("x86_64","amd64"): return "amd64"
    if machine in ("aarch64","arm64"): return "arm64"
    raise ReleaseError("Arquitectura no compatible. Se requiere amd64 o arm64.")
def _read_url(url,limit):
    with _request(url) as response: data=response.read(limit+1)
    if len(data)>limit: raise ReleaseError("Respuesta del repositorio demasiado grande.")
    return data
def _verify_repository(work,status=None):
    import re, shutil, subprocess
    for command in ("gpg","gpgv"):
        if not shutil.which(command): raise ReleaseError("Falta %s. No se puede verificar el repositorio."%command)
    if status: status("Descargando clave e índice firmado de Anthropic…")
    key=work/"anthropic-key.asc"; signed=work/"InRelease"; verified=work/"Release.verified"
    key.write_bytes(_read_url(KEY_URL,262144))
    signed.write_bytes(_read_url(BASE_URL+"/dists/stable/InRelease",2*1024*1024))
    shown=subprocess.run(["gpg","--show-keys","--with-colons",str(key)],capture_output=True,text=True,timeout=20)
    fingerprints=re.findall(r"^fpr:::::::::([0-9A-F]+):?$",shown.stdout,re.M)
    if shown.returncode or EXPECTED_FINGERPRINT not in fingerprints:
        raise ReleaseError("La huella de la clave de Anthropic no coincide. Descarga cancelada.")
    keyring=work/"anthropic-keyring.gpg"
    converted=subprocess.run(["gpg","--batch","--yes","--dearmor","--output",str(keyring),str(key)],capture_output=True,text=True,timeout=20)
    if converted.returncode: raise ReleaseError("No se pudo preparar la clave oficial.")
    check=subprocess.run(["gpgv","--output",str(verified),"--keyring",str(keyring),str(signed)],capture_output=True,text=True,timeout=30)
    if check.returncode: raise ReleaseError("Firma de Anthropic no válida: "+(check.stderr or "")[-800:])
    return verified.read_text(encoding="utf-8",errors="replace")
def _index_digest(release_text,relative_path):
    inside=False
    for line in release_text.splitlines():
        if line.strip()=="SHA256:": inside=True; continue
        if inside:
            if not line.startswith(" "): break
            parts=line.split()
            if len(parts)==3 and parts[2]==relative_path:
                if re.fullmatch(r"[0-9a-fA-F]{64}",parts[0]): return parts[0].lower()
                break
    raise ReleaseError("El manifiesto firmado no contiene el SHA-256 del índice Packages.")
def _parse_package(index,arch):
    matches=[]
    for stanza in re.split(r"\n\s*\n",index.strip()):
        fields={}
        for line in stanza.splitlines():
            if line and not line[0].isspace() and ":" in line:
                key,value=line.split(":",1); fields[key]=value.strip()
        if fields.get("Package")=="claude-desktop" and fields.get("Architecture")==arch: matches.append(fields)
    if not matches: raise ReleaseError("Anthropic no publica Claude Desktop para %s."%arch)
    item=matches[-1]
    for key in ("Version","Filename","SHA256","Size"):
        if key not in item: raise ReleaseError("Falta el campo %s en el índice oficial."%key)
    if not re.fullmatch(r"[0-9a-fA-F]{64}",item["SHA256"]) or not item["Size"].isdigit():
        raise ReleaseError("Metadatos de integridad/tamaño no válidos.")
    size=int(item["Size"])
    if size<=0 or size>MAX_PACKAGE_BYTES: raise ReleaseError("Tamaño del paquete fuera de límites.")
    filename=item["Filename"]
    if filename.startswith("/") or ".." in Path(filename).parts: raise ReleaseError("Ruta del paquete no válida.")
    return item
def get_latest_package(work,status=None):
    import hashlib
    arch=architecture(); release=_verify_repository(work,status)
    relative="main/binary-%s/Packages"%arch
    if status: status("Verificando índice Packages con el manifiesto firmado…")
    index=_read_url(BASE_URL+"/dists/stable/"+relative,MAX_INDEX_BYTES)
    if hashlib.sha256(index).hexdigest()!=_index_digest(release,relative):
        raise ReleaseError("El índice Packages no coincide con el SHA-256 del manifiesto firmado.")
    item=_parse_package(index.decode("utf-8",errors="replace"),arch)
    return PackageInfo(item["Version"],arch,item["Filename"],item["SHA256"].lower(),int(item["Size"]),BASE_URL+"/"+item["Filename"])
def download_verified(package,destination,progress=None):
    import hashlib
    destination.parent.mkdir(parents=True,exist_ok=True); temporary=destination.with_suffix(destination.suffix+".part")
    digest=hashlib.sha256(); received=0
    try:
        with _request(package.url,90) as response,temporary.open("wb") as output:
            while True:
                chunk=response.read(1024*1024)
                if not chunk: break
                received+=len(chunk)
                if received>package.size or received>MAX_PACKAGE_BYTES: raise ReleaseError("La descarga supera el tamaño publicado.")
                output.write(chunk); digest.update(chunk)
                if progress: progress(received,package.size)
        if received!=package.size: raise ReleaseError("Descarga incompleta: %d de %d bytes."%(received,package.size))
        if digest.hexdigest()!=package.sha256: raise ReleaseError("El SHA-256 del paquete no coincide con el índice firmado.")
        temporary.replace(destination); destination.chmod(0o600); return destination
    except Exception:
        try: temporary.unlink()
        except OSError: pass
        raise
