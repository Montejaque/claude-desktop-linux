# Claude Desktop Linux Installer

Instalador gráfico independiente para instalar Claude Desktop en el perfil del usuario Linux, sin permisos root.

> **Importante:** la vía incluida para Ubuntu 20.04 utiliza un AppImage comunitario no oficial. No está respaldada por Anthropic. El paquete se descarga desde GitHub Releases y se valida con el SHA-256 publicado para ese asset.

## Funciones

- Interfaz gráfica en español, con tema oscuro y acento amarillo.
- Detecta distribución, arquitectura, kernel, sesión gráfica y glibc.
- Descarga la última versión comunitaria publicada para amd64 o arm64.
- Comprueba URL de origen, tamaño y SHA-256 antes de extraer el archivo.
- Instala solo en `~/.local/opt`.
- Crea lanzador de Claude en el menú GNOME y copia el icono incluido en el paquete.
- Permite abrir, actualizar y desinstalar.
- Conserva la configuración personal de Claude al desinstalar.
- No utiliza sudo, no instala paquetes del sistema y no modifica glibc.

## Requisitos

- Linux x86_64 o ARM64.
- Python 3 y Tkinter.
- Conexión HTTPS a GitHub.
- Espacio libre de varios cientos de MB para descargar y extraer la aplicación.

## Ejecutar

```bash
bash scripts/run-local.sh
```

Para crear un comando de usuario:

```bash
bash scripts/install-launcher.sh
```

Después ejecuta:

```bash
~/.local/bin/claude-desktop-installer
```

## Fuente del paquete comunitario

- Proyecto: https://github.com/aaddrick/claude-desktop-debian
- Última release: https://github.com/aaddrick/claude-desktop-debian/releases/latest

Este proyecto de Montejaque no mantiene ni firma el AppImage. Se verifica su SHA-256 contra el digest publicado por GitHub para el asset de la release consultada.

## Compatibilidad oficial

Anthropic documenta Linux beta para Ubuntu 22.04 LTS o posterior y Debian 12 o posterior, en x64 y arm64. Ubuntu 20.04 no está en esa lista. Por eso el instalador no intenta forzar el paquete oficial ni sustituir bibliotecas del sistema.

## Documentación

Consulta [docs/INSTALLATION.md](docs/INSTALLATION.md) y [SECURITY.md](SECURITY.md).
