# Claude Desktop Installer para Linux

**Versión 1.0.1**

Instalador gráfico independiente para **Claude Desktop oficial de Anthropic**. Descarga el paquete DEB desde el repositorio APT oficial, verifica la firma GPG del manifiesto, el SHA-256 del índice y el SHA-256 del paquete y lo extrae en el perfil del usuario, sin sudo.

## Funciones
- Interfaz gráfica en español, con identidad visual blanca y amarilla.
- Verificación de la huella de la clave de Anthropic, firma InRelease, hash del índice Packages y hash del DEB.
- Instalación y actualización en `~/.local/opt/claude-desktop`.
- Creación del lanzador de escritorio, icono y asociación del protocolo `claude://`.
- Reparación del acceso, comprobación de versión y desinstalación no destructiva.
- AppImage del instalador y documentación de usuario y técnica.

## Compatibilidad
El paquete oficial consultado declara `libc6 >= 2.34`. Ubuntu 20.04 normalmente incorpora glibc 2.31 y queda fuera de ese requisito. El instalador avisa y permite continuar bajo responsabilidad del usuario, sin modificar glibc ni bibliotecas del sistema. En el equipo de pruebas de Montejaque, el paquete oficial se extrajo y abrió en Ubuntu 20.04; esto no equivale a soporte oficial ni garantiza futuras versiones.

## Ejecución desde el código
```bash
python3 -m claude_installer.app
```

Requisitos: Python 3.8 o superior, Tkinter, `gpg`, `gpgv` y `dpkg-deb`.

## Construir la AppImage y la guía PDF
Consulta [Construcción de AppImage](docs/BUILD_APPIMAGE.md). La AppImage contiene el instalador; Claude Desktop se descarga directamente de Anthropic al instalar.

## Documentación
- [Guía de ayuda](docs/GUIA_USUARIO.md)
- [Instalación y arquitectura técnica](docs/INSTALACION.md)
- [Construcción de AppImage y PDF](docs/BUILD_APPIMAGE.md)
- [Política de seguridad](SECURITY.md)
- [Historial de cambios](CHANGELOG.md)

## Desarrollador y contacto
**Desarrollador: Francisco Javier Gallego Orellana**  
**Punto Vuela Montejaque**  
Avenida Andalucía, 48 · 29360 Montejaque (Málaga)  
Teléfono: 633 402 959  
Correo: montejaque@puntosvuela.es  
Web: https://puntosvuela.es/centros/montejaque

Claude y Anthropic son marcas de sus respectivos titulares. Este instalador es un proyecto independiente, no afiliado, patrocinado ni certificado por Anthropic.
