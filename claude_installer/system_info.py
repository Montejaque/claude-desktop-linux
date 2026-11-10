"""Read-only Linux system diagnostics.

This module never modifies the host system and has no third-party dependencies.
"""
from __future__ import annotations

import platform
import re
import shutil
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Optional, Tuple


@dataclass(frozen=True)
class SystemInfo:
    distro_id: str
    distro_name: str
    distro_version: str
    architecture: str
    kernel: str
    desktop: str
    session_type: str
    glibc_version: Optional[str]
    glibc_supported_for_official_linux_build: Optional[bool]
    has_apt: bool
    has_dpkg: bool

    def to_dict(self) -> Dict[str, object]:
        return asdict(self)


def _os_release() -> Dict[str, str]:
    values: Dict[str, str] = {}
    path = Path("/etc/os-release")
    try:
        for raw_line in path.read_text(encoding="utf-8").splitlines():
            if "=" not in raw_line or raw_line.startswith("#"):
                continue
            key, value = raw_line.split("=", 1)
            values[key] = value.strip().strip('"').strip("'")
    except OSError:
        pass
    return values


def _glibc_version() -> Optional[str]:
    try:
        result = subprocess.run(
            ["getconf", "GNU_LIBC_VERSION"],
            check=True, capture_output=True, text=True, timeout=3,
        )
        match = re.search(r"(\d+)\.(\d+)", result.stdout)
        return ".".join(match.groups()) if match else None
    except (OSError, subprocess.SubprocessError):
        return None


def _version_at_least(actual: Optional[str], required: Tuple[int, int]) -> Optional[bool]:
    if not actual:
        return None
    match = re.match(r"^(\d+)\.(\d+)", actual)
    if not match:
        return None
    return tuple(map(int, match.groups())) >= required


def inspect_system() -> SystemInfo:
    release = _os_release()
    distro_id = release.get("ID", "unknown").lower()
    version = release.get("VERSION_ID", "unknown")
    glibc = _glibc_version()
    return SystemInfo(
        distro_id=distro_id,
        distro_name=release.get("PRETTY_NAME", platform.platform()),
        distro_version=version,
        architecture=platform.machine(),
        kernel=platform.release(),
        desktop=(
            __import__("os").environ.get("XDG_CURRENT_DESKTOP", "unknown")
        ),
        session_type=(
            __import__("os").environ.get("XDG_SESSION_TYPE", "unknown")
        ),
        glibc_version=glibc,
        # Current official Linux desktop package baseline: glibc 2.34.
        glibc_supported_for_official_linux_build=_version_at_least(glibc, (2, 34)),
        has_apt=shutil.which("apt") is not None,
        has_dpkg=shutil.which("dpkg") is not None,
    )


def compatibility_summary(info: Optional[SystemInfo] = None) -> Dict[str, object]:
    info = info or inspect_system()
    arch_ok = info.architecture in ("x86_64", "aarch64")
    glibc_ok = info.glibc_supported_for_official_linux_build
    compatible = arch_ok and glibc_ok is True
    reasons = []
    if not arch_ok:
        reasons.append("La arquitectura no está entre las arquitecturas Linux admitidas.")
    if glibc_ok is False:
        reasons.append(
            "La versión de glibc es inferior a 2.34; el paquete oficial actual "
            "no debe instalarse en este sistema."
        )
    elif glibc_ok is None:
        reasons.append("No se ha podido determinar la versión de glibc.")
    return {
        "compatible_with_current_official_baseline": compatible,
        "reasons": reasons,
        "system": info.to_dict(),
    }
