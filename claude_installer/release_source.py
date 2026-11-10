"""Fetch and verify the latest community AppImage release.

The AppImage is built by a third-party project, not Anthropic. We only accept
assets from its canonical GitHub release API and require GitHub's SHA-256 digest.
"""
from __future__ import annotations

import hashlib
import json
import platform
import re
import shutil
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

RELEASE_API = "https://api.github.com/repos/aaddrick/claude-desktop-debian/releases/latest"
USER_AGENT = "Montejaque-Claude-Desktop-Installer/0.2.0"
MAX_DOWNLOAD_BYTES = 600 * 1024 * 1024


class ReleaseError(RuntimeError):
    pass


@dataclass(frozen=True)
class ReleaseAsset:
    version: str
    name: str
    url: str
    sha256: str
    size: int


def _request(url: str, timeout: int = 30):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/vnd.github+json",
        },
    )
    return urllib.request.urlopen(req, timeout=timeout)


def architecture_asset() -> str:
    machine = platform.machine().lower()
    if machine in ("x86_64", "amd64"):
        return "amd64"
    if machine in ("aarch64", "arm64"):
        return "arm64"
    raise ReleaseError("Arquitectura no compatible con las versiones publicadas (amd64/arm64).")


def get_latest_asset() -> ReleaseAsset:
    arch = architecture_asset()
    try:
        with _request(RELEASE_API) as response:
            release = json.loads(response.read(2 * 1024 * 1024).decode("utf-8"))
    except Exception as exc:
        raise ReleaseError("No se pudo consultar la última versión en GitHub: %s" % exc)

    tag = release.get("tag_name")
    if not isinstance(tag, str) or not tag:
        raise ReleaseError("La respuesta de GitHub no contiene una versión válida.")

    expected_suffix = "-%s.AppImage" % arch
    candidates = [
        asset for asset in release.get("assets", [])
        if isinstance(asset.get("name"), str)
        and asset["name"].endswith(expected_suffix)
        and asset["name"].startswith("claude-desktop-unofficial-")
        and isinstance(asset.get("digest"), str)
        and re.fullmatch(r"sha256:[0-9a-fA-F]{64}", asset["digest"])
    ]
    if len(candidates) != 1:
        raise ReleaseError("No se encontró un único AppImage verificable para %s." % arch)

    asset = candidates[0]
    size = int(asset.get("size") or 0)
    url = asset.get("browser_download_url")
    if not url or not url.startswith(
        "https://github.com/aaddrick/claude-desktop-debian/releases/download/"
    ):
        raise ReleaseError("La URL de descarga no pertenece al repositorio esperado.")
    if size <= 0 or size > MAX_DOWNLOAD_BYTES:
        raise ReleaseError("El tamaño publicado del archivo no es válido.")
    return ReleaseAsset(
        version=tag,
        name=asset["name"],
        url=url,
        sha256=asset["digest"].split(":", 1)[1].lower(),
        size=size,
    )


def download_verified(asset: ReleaseAsset, destination: Path, progress=None) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".part")
    digest = hashlib.sha256()
    received = 0
    try:
        with _request(asset.url, timeout=60) as response, temporary.open("wb") as output:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                received += len(chunk)
                if received > MAX_DOWNLOAD_BYTES or received > asset.size:
                    raise ReleaseError("La descarga supera el tamaño publicado.")
                output.write(chunk)
                digest.update(chunk)
                if progress:
                    progress(received, asset.size)
        if received != asset.size:
            raise ReleaseError("La descarga está incompleta (%d de %d bytes)." % (received, asset.size))
        actual = digest.hexdigest()
        if actual != asset.sha256:
            raise ReleaseError("La huella SHA-256 no coincide. El archivo se ha rechazado.")
        temporary.replace(destination)
        destination.chmod(0o700)
        return destination
    except Exception:
        try:
            temporary.unlink()
        except OSError:
            pass
        raise


def has_extractor() -> bool:
    return shutil.which("tar") is not None
