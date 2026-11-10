# Documentación técnica e instalación

## Módulos
- claude_installer/release_source.py: descarga la clave, fija su huella, valida InRelease, el hash del índice Packages y el hash del DEB.
- claude_installer/installer.py: extracción por usuario, wrapper, icono, .desktop, protocolo claude://, actualización con recuperación y desinstalación.
- claude_installer/system_info.py: diagnóstico de distribución, arquitectura, kernel, sesión y glibc.
- claude_installer/app.py: interfaz Tkinter en español.

## Repositorio oficial
Base APT: https://downloads.claude.ai/claude-desktop/apt/stable  
Clave: https://downloads.claude.ai/claude-desktop/key.asc  
Huella fijada: 31DDDE24DDFAB679F42D7BD2BAA929FF1A7ECACE

Cadena de verificación: huella de clave -> firma InRelease -> SHA-256 de Packages -> SHA-256 del DEB. Si falla una comprobación, no se extrae el paquete.

## Rutas
- Aplicación: ~/.local/opt/claude-desktop (compatible con la instalación manual de prueba).
- Wrapper: ~/.local/bin/claude-desktop-oficial
- Lanzador: ~/.local/share/applications/claude-desktop.desktop
- Icono: ~/.local/share/icons/hicolor/256x256/apps/claude-desktop.png
- Caché: ~/.cache/claude-desktop-installer

La configuración personal de Claude no se gestiona ni se elimina. La actualización reutiliza la ruta de la instalación que ya se probó en el equipo.

## Desarrollador y centro
**Francisco Javier Gallego Orellana** · Punto Vuela Montejaque  
Avenida Andalucía, 48 · 29360 Montejaque (Málaga)  
633 402 959 · montejaque@puntosvuela.es  
https://puntosvuela.es/centros/montejaque

## Desarrollo
\`\`\`bash
python3 -m tkinter
python3 -m claude_installer.app
python3 -m unittest discover -s tests -v
\`\`\`
Dependencias del host: Python/Tkinter, gpg, gpgv y dpkg-deb. Sin dependencias Python externas en ejecución.
