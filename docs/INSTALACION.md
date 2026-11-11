# Instalación y arquitectura técnica

**Claude Desktop Installer para Linux · Versión 1.0.3**

## Arquitectura
- `claude_installer/release_source.py`: descarga la clave y los metadatos del repositorio oficial; fija la huella y valida la firma de `InRelease`, el hash del índice `Packages` y el hash del paquete DEB.
- `claude_installer/installer.py`: descarga y extrae el paquete en el perfil del usuario; crea wrapper, icono, lanzador `.desktop` y protocolo `claude://`; gestiona actualización, recuperación y desinstalación.
- `claude_installer/system_info.py`: diagnóstico de distribución, arquitectura, kernel, sesión gráfica y versión de glibc.
- `claude_installer/app.py`: interfaz gráfica Tkinter en español.

## Fuente oficial y verificación
Repositorio APT: https://downloads.claude.ai/claude-desktop/apt/stable  
Clave pública: https://downloads.claude.ai/claude-desktop/key.asc  
Huella fijada: `31DDDE24DDFAB679F42D7BD2BAA929FF1A7ECACE`

Cadena de confianza:
1. Se comprueba que la clave descargada coincide con la huella fijada.
2. Se verifica la firma OpenPGP del fichero `InRelease`.
3. Se compara el SHA-256 del índice `Packages` con el valor del manifiesto firmado.
4. Se compara el SHA-256 del paquete DEB con el índice firmado.
5. Solo tras superar todas las comprobaciones se extrae el paquete.

Si falla una comprobación, el proceso se detiene.

## Instalación por usuario
- Aplicación: `~/.local/opt/claude-desktop`
- Wrapper: `~/.local/bin/claude-desktop-oficial`
- Lanzador: `~/.local/share/applications/claude-desktop.desktop`
- Icono: `~/.local/share/icons/hicolor/256x256/apps/claude-desktop.png`
- Caché: `~/.cache/claude-desktop-installer`

No se utiliza `sudo`, no se ejecutan scripts de mantenimiento del DEB y no se modifica `/usr`, glibc ni las bibliotecas del sistema. La configuración personal de Claude se conserva al actualizar o desinstalar.

## Compatibilidad
El paquete oficial consultado declara `libc6 >= 2.34`. Ubuntu 20.04 suele incluir glibc 2.31 y queda fuera de ese requisito. La aplicación avisa antes de continuar. La prueba local de extracción y arranque en Ubuntu 20.04 no constituye soporte oficial ni garantiza compatibilidad futura.

## Desarrollador y centro
**Francisco Javier Gallego Orellana** · **Punto Vuela Montejaque**  
Avenida Andalucía, 48 · 29360 Montejaque (Málaga)  
Teléfono: 633 402 959  
Correo: montejaque@puntosvuela.es  
Web: https://puntosvuela.es/centros/montejaque

## Desarrollo y pruebas
```bash
python3 -m tkinter
python3 -m claude_installer.app
python3 -m unittest discover -s tests -v
```

Dependencias de ejecución del sistema: Python/Tkinter, `gpg`, `gpgv` y `dpkg-deb`. No requiere dependencias Python externas para la ejecución normal.
