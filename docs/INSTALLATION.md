# Instalación y uso

## Qué instala

La aplicación instala una compilación AppImage comunitaria de Claude Desktop. No es un paquete oficial de Anthropic.

Fuente del paquete:
- Repositorio: https://github.com/aaddrick/claude-desktop-debian
- API de releases: https://api.github.com/repos/aaddrick/claude-desktop-debian/releases/latest

El instalador solo acepta assets AppImage con el nombre esperado, una URL de descarga del repositorio anterior y un SHA-256 publicado por GitHub Releases. Descarga el archivo completo, calcula SHA-256 y no lo extrae si la huella no coincide.

## Requisitos

- Linux x86_64/amd64 o ARM64.
- Python 3 con Tkinter.
- Conexión HTTPS a GitHub.
- Espacio libre suficiente para descargar y extraer el paquete (varios cientos de MB).
- Sesión gráfica GNOME/X11 o entorno compatible.

## Ejecutar desde el repositorio

```bash
bash scripts/run-local.sh
```

Para crear un comando en `~/.local/bin`:

```bash
bash scripts/install-launcher.sh
```

No necesita sudo. Si `~/.local/bin` no está en PATH, añade esa ruta a tu configuración de shell.

## Ubicaciones

- Aplicación: `~/.local/opt/claude-desktop-unofficial`
- Lanzador GNOME: `~/.local/share/applications/claude-desktop-unofficial.desktop`
- Icono: `~/.local/share/icons/hicolor/256x256/apps/claude-desktop-unofficial.png`
- Caché de descarga: `~/.cache/claude-desktop-unofficial`

## Actualizar

Pulsa **Instalar / actualizar**. Se consulta la última release, se descarga y verifica el nuevo AppImage y se reemplaza la versión anterior. Si la extracción o instalación falla, se intenta restaurar la instalación previa.

## Desinstalar

Pulsa **Desinstalar** en la aplicación. Se elimina solo el directorio instalado por este instalador, el lanzador y el icono. La configuración de Claude en `~/.config/Claude` se conserva.

## Limitación Ubuntu 20.04

Anthropic documenta Ubuntu 22.04 LTS o posterior y Debian 12 o posterior como requisitos de su app Linux beta. En Ubuntu 20.04 se ofrece únicamente el paquete AppImage comunitario, sin garantía ni soporte de Anthropic. La disponibilidad del AppImage no demuestra por sí sola que todas las funciones vayan a funcionar en todos los escritorios.

El instalador no modifica glibc, no instala paquetes del sistema, no usa sudo y no altera bibliotecas del sistema.
